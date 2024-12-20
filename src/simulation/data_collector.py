import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class DataCollector:
    def __init__(self):
        self.order_book_data = []
        self.bot_data = {}
        self.time_data = []

    def collect_order_book_data(self, market, timestamp):
        bids, asks = market.order_book.get_book_depth(depth=5)
        bids_list = []
        asks_list = []
        for bid in bids:
            bid_tuple = (bid.price, bid.quantity)
            bids_list.append(bid_tuple)
        for ask in asks:
            ask_tuple = (ask.price, ask.quantity)
            asks_list.append(ask_tuple)
        self.order_book_data.append({
            'timestamp': timestamp, 
            'bids': bids_list, 
            'asks': asks_list
            }
        )
    
    def collect_bot_data(self, bot, timestamp):
        if bot.bot_id not in self.bot_data:
            self.bot_data[bot.bot_id] = {
                'cash': [],
                'inventory': [],
                'time': []
            }
        self.bot_data[bot.bot_id]['cash'].append(bot.cash)
        self.bot_data[bot.bot_id]['inventory'].append(bot.inventory)
        self.bot_data[bot.bot_id]['time'].append(timestamp)
    
    def collect_time_data(self, timestamp):
        self.time_data.append(timestamp)