from bots.base_bot import BaseBot
import random

class RandomBot(BaseBot):
    def __init__(self, order_interval=10, order_quantity=10, max_price=100, **kwargs):
        super().__init__(**kwargs)
        self.order_interval = order_interval
        self.order_quantity = order_quantity
        self.max_price = max_price
        self.last_order_time = 0
        self.type = "random"

    def act(self, market, timestamp):
        if timestamp - self.last_order_time >= self.order_interval:
            order_type = random.choice(["buy", "sell"])
            price = random.uniform(1, self.max_price)
            quantity = self.order_quantity

            self.place_order(market, order_type, price, quantity, timestamp)
            self.last_order_time = timestamp
