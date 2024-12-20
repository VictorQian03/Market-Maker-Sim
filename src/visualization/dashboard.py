import matplotlib.pyplot as plt
from visualization.chart_plotter import ChartPlotter

class Dashboard:
    def __init__(self, data_collector):
        self.data_collector = data_collector

    def plot_all(self):
        fig, axs = plt.subplots(3, 1, figsize=(10, 15))
        ChartPlotter.plot_order_book(self.data_collector.order_book_data, axs[0])
        ChartPlotter.plot_bot_pnl(self.data_collector.bot_data, axs[1])
        ChartPlotter.plot_bot_inventory(self.data_collector.bot_data, axs[2])
        plt.tight_layout(pad=3.0)
        plt.show()