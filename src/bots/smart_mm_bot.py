import random
from bots.base_bot import BaseBot

class SmartMMBot(BaseBot):
    def __init__(
        self,
        spread=1,
        order_quantity=10,
        inventory_target=0,
        max_inventory=50, 
        spread_inventory_factor=0.1,
        spread_pnl_factor=0.05,
        size_inventory_factor=0.1,
        size_variance=5,
        pnl_widen_threshold=-100,
        widen_multiplier=2,
        lookback_window=10,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.spread = spread
        self.order_quantity = order_quantity
        self.inventory_target = inventory_target
        self.max_inventory = max_inventory
        self.spread_inventory_factor = spread_inventory_factor
        self.spread_pnl_factor = spread_pnl_factor
        self.size_inventory_factor = size_inventory_factor
        self.size_variance = size_variance
        self.pnl_widen_threshold = pnl_widen_threshold
        self.widen_multiplier = widen_multiplier
        self.lookback_window = lookback_window
        self.realized_pnl = 0
        self.has_placed_initial_orders = False
        self.type = "smart"

    def on_trade(self, trade):
        super().on_trade(trade)
        if trade.buyer_id == self.bot_id:
            self.realized_pnl -= trade.price * trade.quantity
        elif trade.seller_id == self.bot_id:
            self.realized_pnl += trade.price * trade.quantity
    
    def compute_adaptive_spread(self):
        inventory_deviation = abs(self.inventory - self.inventory_target)
        inventory_spread_penalty = inventory_deviation * self.spread_inventory_factor
        # Up on PnL, tighten spread; down on PnL, widen spread
        pnl_component = -self.realized_pnl * self.spread_pnl_factor
        spread = self.spread + inventory_spread_penalty + pnl_component
        if self.realized_pnl < self.pnl_widen_threshold:
            spread *= self.widen_multiplier
        spread = max(spread, 0.01)
        return spread
    
    def compute_order_quantity(self):
        if abs(self.inventory) >= self.max_inventory:
            return 1
        inventory_deviation = abs(self.inventory - self.inventory_target)
        # Larger the deviation, the smaller the new order sizes
        scale_factor = 1 / (1 + inventory_deviation * self.size_inventory_factor)
        size = int(self.order_quantity * scale_factor)
        size += random.randint(-self.size_variance, self.size_variance)
        size = max(size, 1)
        return size
    
    def act(self, market, timestamp):
        if not self.has_placed_initial_orders:
            buy_price = 50 - self.spread / 2
            sell_price = 50 + self.spread / 2
            initial_quantity = self.order_quantity + random.randint(-self.size_variance, self.size_variance)
            if buy_price > 0:
                self.place_order(market, "buy", buy_price, initial_quantity, timestamp)
            if sell_price > 0:
                self.place_order(market, "sell", sell_price, initial_quantity, timestamp)
            self.has_placed_initial_orders = True
            return  
        for order_id in list(self.orders.keys()):
            if self.orders[order_id].timestamp < timestamp - self.lookback_window:
                self.cancel_order(market, order_id, timestamp)
        spread = self.compute_adaptive_spread()
        order_quantity = self.compute_order_quantity()
        mid_price = market.order_book.get_mid_price()
        if mid_price is None:
            return
        buy_price = max(mid_price - spread / 2, 0.01)
        sell_price = max(mid_price + spread / 2, 0.01)
        self.place_order(market, "buy", buy_price, order_quantity, timestamp)
        self.place_order(market, "sell", sell_price, order_quantity, timestamp)

