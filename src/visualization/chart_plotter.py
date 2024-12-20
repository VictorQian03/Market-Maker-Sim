import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

class ChartPlotter:
    @staticmethod
    def plot_order_book(order_book_data, ax):
        timestamps = [entry['timestamp'] for entry in order_book_data]
        
        bid_prices = [[(price, qty) for price, qty in entry['bids']] for entry in order_book_data]
        ask_prices = [[(price, qty) for price, qty in entry['asks']] for entry in order_book_data]

        bid_price_series = []
        bid_qty_series = []
        ask_price_series = []
        ask_qty_series = []
        for bid_set, ask_set in zip(bid_prices, ask_prices):
            if bid_set:
                bid_price_series.append([price for price, _ in bid_set])
                bid_qty_series.append([qty for _, qty in bid_set])
            else:
                bid_price_series.append([])
                bid_qty_series.append([])
            if ask_set:
                ask_price_series.append([price for price, _ in ask_set])
                ask_qty_series.append([qty for _, qty in ask_set])
            else:
                ask_price_series.append([])
                ask_qty_series.append([])

        ax.set_title('Order Book Evolution')
        ax.set_xlabel('Time Step')
        ax.set_ylabel('Price')

        for i, bid_prices_time in enumerate(bid_price_series):
          for j, bid_price in enumerate(bid_prices_time):
              ax.plot(timestamps[i], bid_price, 'g.', label=f'Bid {j+1}' if i == 0 else "")
        
        for i, ask_prices_time in enumerate(ask_price_series):
          for j, ask_price in enumerate(ask_prices_time):
              ax.plot(timestamps[i], ask_price, 'r.', label=f'Ask {j+1}' if i == 0 else "")
        
        ax.legend()

    
    @staticmethod
    def plot_bot_pnl(bot_data, ax):
        for bot_id, data in bot_data.items():
            ax.plot(data['time'], data['cash'], label=f'Bot {bot_id}')
        ax.set_title('Bot PnL Evolution')
        ax.set_xlabel('Time Step')
        ax.set_ylabel('PnL')
        ax.legend()
    
    @staticmethod
    def plot_bot_inventory(bot_data, ax):
        for bot_id, data in bot_data.items():
            ax.plot(data['time'], data['inventory'], label=f'Bot {bot_id}')
        ax.set_title('Bot Inventory Evolution')
        ax.set_xlabel('Time Step')
        ax.set_ylabel('Inventory')
        ax.legend()
            
        