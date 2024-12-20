from core.time_event import TimeEvent

def calculate_pnl(bot):
    return bot.cash

def calculate_inventory(bot):
    return bot.inventory

def calculate_activity(bot, all_events):
    bot_order_ids = bot.get_unfilled_orders().keys()

    bot_events_count = 0
    for event in all_events:
        if isinstance(event, TimeEvent):
            continue
        for order in bot_order_ids:
            if event.timestamp >= 0:
                bot_events_count += 1
    
    total_events = len(all_events)
    if total_events == 0:
        return 0
    return bot_events_count / total_events