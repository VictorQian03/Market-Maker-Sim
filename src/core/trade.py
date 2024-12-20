class Trade:
    def __init__(self, buyer_id, seller_id, price, quantity, timestamp):
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.price = price
        self.quantity = quantity
        self.timestamp = timestamp
        
    def __repr__(self):
        return f"Trade(buyer_id={self.buyer_id}, seller_id={self.seller_id}, price={self.price}, qty={self.quantity})"