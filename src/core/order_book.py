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
        self.bids = [] # Descending order sorted
        self.asks = [] # Ascending order sorted
        self.order_map = {}
        self.order_id_counter = 0

    def get_next_order_id(self):
        self.order_id_counter += 1
        return self.order_id_counter
    
    def add_order(self, order_type, price, quantity, bot_id,
                  timestamp):
        order_id = self.order_id_counter
        order = Order(order_id, order_type, price, quantity, bot_id, timestamp)
        self.order_map[order_id] = order

        if order_type == "buy":
            self.bids.append(order)
            self.bids.sort(key = lambda x: x.price, reverse=True)
        elif order_type == "sell":
            self.asks.append(order)
            self.asks.sort(key = lambda x: x.price)
        return order
    
    def remove_order(self, order_id):
        if order_id in self.order_map:
            order = self.order_map[order_id]
            del self.order_map[order_id]
            if order.order_type == "buy":
                filtered_bids = []
                for i in self.bids:
                    if i.order_id != order_id:
                        filtered_bids.append(i)
                self.bids = filtered_bids
            elif order.order_type == "sell":
                filtered_asks = []
                for i in self.asks:
                    if i.order_id != order_id:
                        filtered_asks.append(i)
                self.asks = filtered_asks
    
    def match_orders(self):
        trades = []
        while self.bids and self.asks and self.bids[0].price >= self.asks[0].price:
            best_bid = self.bids[0]
            best_ask = self.asks[0]

            trade_quantity = min(best_bid.quantity, best_ask.quantity)
            trade_price = best_ask.price # Assume ask price always wins 

            trades.append((best_bid.bot_id, best_ask.bot_id, trade_price, trade_quantity))

            best_bid.quantity -= trade_quantity
            best_ask.quantity -= trade_quantity

            if best_bid.quantity == 0:
                self.remove_order(best_bid.order_id)
            if best_ask.quantity == 0:
                self.remove_order(best_ask.order_id)
        return trades
    
    def get_best_bid(self):
        if self.bids:
            return self.bids[0].price
        
    def get_best_ask(self):
        if self.asks:
            return self.asks[0].price
    
    def get_mid_price(self):
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()
        if best_bid is None or best_ask is None:
            return None
        else:
            return (best_bid + best_ask) / 2
    
    def get_book_depth(self, depth):
        bids = self.bids[:depth]
        asks = self.asks[:depth]
        return bids, asks

    def __str__(self):
        bids_list = []
        for b in self.bids:
            bids_list.append(b)
        asks_list = []
        for a in self.asks:
            asks_list.append(a)
        return f"Bids: {bids_list}, Asks: {asks_list}"
                