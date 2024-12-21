import bisect
import uuid

class Order:
    def __init__(self, order_id, order_type, price, quantity, bot_id, timestamp):
        self.order_id = order_id
        self.order_type = order_type
        self.price = price
        self.quantity = quantity
        self.bot_id = bot_id
        self.timestamp = timestamp

    def __repr__(self):
      return f"Order(id={self.order_id}, type={self.order_type}, price={self.price}, qty={self.quantity}, bot_id={self.bot_id})"

class OrderBook:
    def __init__(self):
        self.bids = {}
        self.asks = {}
        
        self.bid_prices = []  
        self.ask_prices = []  
        
        self.order_map = {}
        self.order_id_counter = 0

    def get_next_order_id(self):
        self.order_id_counter += 1
        return self.order_id_counter

    def _add_price_level(self, price_list, price):
        bisect.insort(price_list, price)

    def _remove_price_level(self, price_list, price):
        idx = bisect.bisect_left(price_list, price)
        if idx < len(price_list) and price_list[idx] == price:
            price_list.pop(idx)

    def add_order(self, order_type, price, quantity, bot_id, timestamp):
        order_id = self.get_next_order_id()
        order = Order(order_id, order_type, price, quantity, bot_id, timestamp)
        self.order_map[order_id] = order

        if order_type == "buy":
            if price not in self.bids:
                self.bids[price] = []
                self._add_price_level(self.bid_prices, price)
            self.bids[price].append(order)
        else:  
            if price not in self.asks:
                self.asks[price] = []
                self._add_price_level(self.ask_prices, price)
            self.asks[price].append(order)

        return order

    def remove_order(self, order_id):
        if order_id not in self.order_map:
            return
        
        order = self.order_map[order_id]
        del self.order_map[order_id]

        if order.order_type == "buy":
            orders_at_price = self.bids[order.price]
            updated_orders = []
            for o in orders_at_price:
                if o.order_id != order_id:
                    updated_orders.append(o)
            self.bids[order.price] = updated_orders
            if not self.bids[order.price]:
                del self.bids[order.price]
                self._remove_price_level(self.bid_prices, order.price)
        else:
            orders_at_price = self.asks[order.price]
            updated_orders = []
            for o in orders_at_price:
                if o.order_id != order_id:
                    updated_orders.append(o)
            self.asks[order.price] = updated_orders
            if not self.asks[order.price]:
                del self.asks[order.price]
                self._remove_price_level(self.ask_prices, order.price)

    def match_orders(self):
        trades = []
        while self.bid_prices and self.ask_prices:
            best_bid_price = self.get_best_bid() 
            best_ask_price = self.get_best_ask()

            if best_bid_price < best_ask_price:
                break

            bid_orders = self.bids[best_bid_price]
            ask_orders = self.asks[best_ask_price]

            best_bid = bid_orders[0]  
            best_ask = ask_orders[0] 

            trade_quantity = min(best_bid.quantity, best_ask.quantity)
            if best_bid.order_type == 'buy':
                trade_price = best_ask_price
            else:
                trade_price = best_bid_price

            trades.append((best_bid.bot_id, best_ask.bot_id, trade_price, trade_quantity))

            best_bid.quantity -= trade_quantity
            best_ask.quantity -= trade_quantity

            if best_bid.quantity == 0:
                self.remove_order(best_bid.order_id)

            if best_ask.quantity == 0:
                self.remove_order(best_ask.order_id)

        return trades

    def get_best_bid(self):
        if self.bid_prices:
            return self.bid_prices[-1]
        return None

    def get_best_ask(self):
        if self.ask_prices:
            return self.ask_prices[0]
        return None

    def get_mid_price(self):
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()
        if best_bid is None or best_ask is None:
            return None
        return (best_bid + best_ask) / 2

    def get_book_depth(self, depth):
        top_bids = []
        for price in reversed(self.bid_prices):
            top_bids += self.bids[price]
            if len(top_bids) >= depth:
                top_bids = top_bids[:depth]
                break

        top_asks = []
        for price in self.ask_prices:
            top_asks += self.asks[price]
            if len(top_asks) >= depth:
                top_asks = top_asks[:depth]
                break

        return top_bids, top_asks

    def __str__(self):
      return f"Bids: {self.bids}, Asks: {self.asks}"

    