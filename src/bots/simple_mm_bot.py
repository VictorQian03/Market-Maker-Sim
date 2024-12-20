from bots.base_bot import BaseBot
import random

class SimpleMMBot(BaseBot):
    def __init__(self, spread=1, order_quantity=10, lookback_window=10, 
                 order_size_variance=5, **kwargs):
        super().__init__(**kwargs)
        self.spread = spread
        self.order_quantity = order_quantity
        self.lookback_window = lookback_window
        self.order_size_variance = order_size_variance
        self.has_placed_initial_orders = False
        self.type = "simple"
    
    def act(self, market, timestamp):
        if not self.has_placed_initial_orders:
            buy_price = 50 - self.spread / 2 
            sell_price = 50 + self.spread / 2
            
            buy_quantity = self.order_quantity + random.randint(-self.order_size_variance, self.order_size_variance)
            sell_quantity = self.order_quantity + random.randint(-self.order_size_variance, self.order_size_variance)

            self.place_order(market, 'buy', buy_price, buy_quantity, timestamp)
            self.place_order(market, 'sell', sell_price, sell_quantity, timestamp)
            self.has_placed_initial_orders = True

        mid_price = market.order_book.get_mid_price()
        if mid_price is None:
            return

        for order_id in list(self.orders.keys()):
            if self.orders[order_id].timestamp < timestamp - self.lookback_window:
                self.cancel_order(market, order_id, timestamp)

        buy_price = mid_price - self.spread / 2
        sell_price = mid_price + self.spread / 2

        buy_quantity = self.order_quantity + random.randint(-self.order_size_variance,
                                                            self.order_size_variance)
        sell_quantity = self.order_quantity + random.randint(-self.order_size_variance,
                                                            self.order_size_variance)                                        
        if buy_price > 0:
            self.place_order(market, "buy", buy_price, buy_quantity, timestamp)
        
        if sell_price > 0:
            self.place_order(market, "sell", sell_price, sell_quantity, timestamp)