from abc import ABC, abstractmethod
import uuid

class BaseBot(ABC):
    def __init__(self, bot_id=None):
        if bot_id:
            self.bot_id = bot_id
        else:
            self.bot_id = self.generate_uuid()
        self.cash = 0
        self.inventory = 0
        self.orders = {}
    
    def generate_uuid(self):
        return str(uuid.uuid4())
    
    def update_cash(self, amount):
        self.cash += amount
    
    def update_inventory(self, amount):
        self.inventory += amount
    
    def place_order(self, market, order_type, price, quantity, timestamp):
        order = market.place_order(order_type, price, quantity, self.bot_id, timestamp)
        self.orders[order.order_id] = order
        return order
    
    def cancel_order(self, market, order_id, timestamp):
        market.cancel_order(order_id, timestamp)
        if order_id in self.orders:
            del self.orders[order_id]

    def on_trade(self, trade):
        if trade.buyer_id == self.bot_id:
            self.update_cash(-trade.price * trade.quantity)
            self.update_inventory(trade.quantity)
        elif trade.seller_id == self.bot_id:
            self.update_cash(trade.price * trade.quantity)
            self.update_inventory(-trade.quantity)
    
    def get_unfilled_orders(self):
        return self.orders
    
    @abstractmethod
    def act(self, market, timestamp):
        pass