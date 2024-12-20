from bots.base_bot import BaseBot
import random

class TakerBot(BaseBot):
    def __init__(self, order_interval=5, order_quantity=5, **kwargs):
        super().__init__(**kwargs)
        self.order_interval = order_interval
        self.order_quantity = order_quantity
        self.last_order_time = 0
        self.type = "taker"
    
    def act(self, market, timestamp):
        if timestamp - self.last_order_time >= self.order_interval:
            best_bid = market.order_book.get_best_bid()
            best_ask = market.order_book.get_best_ask()
            if best_bid is None or best_ask is None:
                return
            if random.random() < 0.5:
                self.place_order(market, "buy", best_ask, self.order_quantity, timestamp)
            else:
                self.place_order(market, "sell", best_bid, self.order_quantity, timestamp)
            self.last_order_time = timestamp