import time
import random
from core.market import Market
from core.time_event import TimeEvent
from simulation.data_collector import DataCollector

class Simulator:
    def __init__(self, bots, start_time=0, time_step_interval=1, max_time_steps=100):
        self.market = Market()
        self.bots = bots
        self.current_time = start_time
        self.time_step_interval = time_step_interval
        self.max_time_steps = max_time_steps
        self.events = []
        self.data_collector = DataCollector()

    def run(self):
        for _ in range(self.max_time_steps):
            self.time_step()
            self.data_collector.collect_order_book_data(self.market, self.current_time)
            for bot in self.bots:
                self.data_collector.collect_bot_data(bot, self.current_time)
            self.events.append(TimeEvent(self.current_time))
            #time.sleep(0.1)

    def time_step(self):
        random.shuffle(self.bots)
        for bot in self.bots:
            bot.act(self.market, self.current_time)
        self.market.process_orders(self.current_time)
        for trade in self.market.get_trades_since(self.current_time - self.time_step_interval):
            for bot in self.bots:
                bot.on_trade(trade)

        self.current_time += self.time_step_interval