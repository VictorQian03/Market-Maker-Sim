from bots.simple_mm_bot import SimpleMMBot
from bots.random_bot import RandomBot
from simulation.simulator import Simulator
from simulation.metrics import calculate_pnl, calculate_inventory, calculate_activity

if __name__ == "__main__":
    mm_bot = SimpleMMBot(spread=2, order_quantity=5, lookback_window=5, order_size_variance=2)
    random_bot = RandomBot(order_interval=3, order_quantity=5)
    bots = [mm_bot, random_bot]

    simulator = Simulator(bots, max_time_steps=100, time_step_interval=1)
    simulator.run()

    all_events = simulator.market.events
    for bot in bots:
        pnl = calculate_pnl(bot)
        inventory = calculate_inventory(bot)
        activity = calculate_activity(bot, all_events)
        print(f"Bot {bot.bot_id} - PnL: {pnl:.2f}, Inventory: {inventory}, Activity: {activity:.2f}")
