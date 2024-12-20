from bots.simple_mm_bot import SimpleMMBot
from bots.random_bot import RandomBot
from bots.taker_bot import TakerBot
from simulation.simulator import Simulator
from simulation.metrics import calculate_pnl, calculate_inventory, calculate_activity
from visualization.dashboard import Dashboard

if __name__ == "__main__":
    mm_bot = SimpleMMBot(spread=1, order_quantity=5, lookback_window=20, order_size_variance=3)
    random_bot_1 = RandomBot(order_interval=5, order_quantity=5)
    random_bot_2 = RandomBot(order_interval=5, order_quantity=5)
    taker_bot_1 = TakerBot(order_interval=3, order_quantity=5)
    taker_bot_2 = TakerBot(order_interval=2, order_quantity=10)
    bots = [mm_bot, random_bot_1, random_bot_2, taker_bot_1, taker_bot_2]

    simulator = Simulator(bots, max_time_steps=100, time_step_interval=1)
    simulator.run()

    all_events = simulator.market.events
    for bot in bots:
        pnl = calculate_pnl(bot)
        inventory = calculate_inventory(bot)
        activity = calculate_activity(bot, all_events)
        print(f"Bot {bot.bot_id} with {bot.type} type - PnL: {pnl:.2f}, Inventory: {inventory}, Activity: {activity:.2f}")
    dashboard = Dashboard(simulator.data_collector)
    dashboard.plot_all()
