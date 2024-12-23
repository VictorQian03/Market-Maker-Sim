from bots.simple_mm_bot import SimpleMMBot
from bots.random_bot import RandomBot
from bots.taker_bot import TakerBot
from bots.smart_mm_bot import SmartMMBot
from simulation.simulator import Simulator
from simulation.metrics import calculate_pnl, calculate_inventory, calculate_activity
from visualization.dashboard import Dashboard

if __name__ == "__main__":
    simple_bot = SimpleMMBot(spread=2, order_quantity=5, lookback_window=20, order_size_variance=5)
    smart_bot = SmartMMBot(
        spread=2,
        order_quantity=5,
        inventory_target=0,
        max_inventory=50,
        spread_inventory_factor=0.1,
        spread_pnl_factor=0.05,
        size_inventory_factor=0.1,
        size_variance=5,
        pnl_widen_threshold=-100,
        widen_multiplier=2,
        lookback_window=20
    )
    random_bot_1 = RandomBot(order_interval=5, order_quantity=10)
    random_bot_2 = RandomBot(order_interval=5, order_quantity=10)
    taker_bot_1 = TakerBot(order_interval=1, order_quantity=5)
    taker_bot_2 = TakerBot(order_interval=1, order_quantity=10)
    bots = [simple_bot, smart_bot, random_bot_1, random_bot_2, taker_bot_1, taker_bot_2]

    simulator = Simulator(bots, max_time_steps=100, time_step_interval=1)
    simulator.run()

    all_events = simulator.market.events
    for bot in bots:
        pnl = calculate_pnl(bot)
        inventory = calculate_inventory(bot)
        activity = calculate_activity(bot, all_events)
    ranking = sorted(bots, key=lambda x: calculate_pnl(x), reverse=True)
    print("Ranking:")
    print("========")
    for i, bot in enumerate(ranking):
        pnl = calculate_pnl(bot)
        inventory = calculate_inventory(bot)
        activity = calculate_activity(bot, all_events)
        print(f"{i + 1}. Bot {bot.bot_id} with {bot.type} type - PnL: {pnl:.2f}, Inventory: {inventory}, Activity: {activity:.2f}")
    dashboard = Dashboard(simulator.data_collector)
    dashboard.plot_all()
