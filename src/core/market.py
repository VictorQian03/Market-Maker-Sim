from core.order_book import OrderBook
from core.trade import Trade
from core.event import Event
import uuid

class Market:
    def __init__(self):
        self.order_book = OrderBook()
        self.trades = []
        self.events = []

    def place_order(self, order_type, price, quantity, bot_id, timestamp):
      order = self.order_book.add_order(order_type, price, quantity, bot_id, timestamp)
      return order 

    def cancel_order(self, order_id, timestamp):
      self.order_book.remove_order(order_id)
    
    def process_orders(self, timestamp):
      trades = self.order_book.match_orders()
      for buyer_id, seller_id, price, quantity in trades:
          self.trades.append(Trade(buyer_id, seller_id, price, quantity, timestamp))

      self.events.append(Event(timestamp))
    

    def get_trades_since(self, start_timestamp):
        trades_since = []
        for trade in self.trades:
            if trade.timestamp >= start_timestamp:
                trades_since.append(trade)
        return trades_since
    
    def get_events_since(self, start_timestamp):
        events_since = []
        for event in self.events:
            if event.timestamp >= start_timestamp:
                events_since.append(event)
        return events_since
