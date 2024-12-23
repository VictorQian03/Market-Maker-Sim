# Market-Maker-Sim
This repository contains a simulation of a simple market with trading bots. The simulation allows experimentation with different market-making and trading strategies. To run the simulation, execute the main.py file:

This will:
1. Initialize a market environment.
2. Create and start a set of trading bots with defined strategies.
3. Run the simulation for a specified number of time steps.
4. Output the final PnL (Profit and Loss), inventory, and activity of each bot.
5. Display a dashboard with charts showing the evolution of the order book, bot PnL, and inventory over time.

The simulation makes the following assumptions:
1. Discrete Time: The simulation operates in discrete time steps.
2. Price-Time Priority: The order book matches orders based on price and then time of entry.
3. Limit Order Book: Only limit orders can be placed into the book.
4. Trade Execution: Matched orders execute at the best ask price (for buy orders) or best bid price (for sell orders). Execution order is randomized at each time step. 
5. Market Impact: Trades do not have a market impact, other than clearing limit orders.
6. No Transaction Costs: No trading fees or slippage are modeled.

Trading bots:
1. SimpleMMBot: This bot provides liquidity to the market by placing both buy and sell limit orders around the mid-price.
- Parameters:
    - Increasing spread will provide less liquidity but could increase profit per trade.
    - Changing order_quantity affects the size of its quotes.
    - Adjusting lookback_window will determine how often its quotes are updated.
    - Adjusting order_size_variance will introduce variability into order size.
2. RandomBot: This bot places random buy or sell orders at random prices.
- Parameters:
    - Increase order_interval to make it less active.
    - Adjust order_quantity to change the order sizes.
    - Change max_price to change the price of the random orders.
3. TakerBot: This bot places market orders to immediately consume liquidity from the order book 
- Parameters:
    - Adjust order_interval to change its frequency.
    - Change order_quantity to change the order size.
    - Change time_offset_interval to change it's trade timing.
4. SmartMMBot: A more adaptive market maker that adjusts both its spread and order size based on inventory levels and realized PnL. It continually tries to manage risk by widening quotes if its inventory grows too large or if its PnL drops, and narrowing quotes when conditions improve.
- Parameters:
    - spread: Wider spreads reduce fill frequency but can yield higher profit per trade.
    - order_quantity: Higher quantities mean more potential profit and risk on each trade.
    - inventory_target and max_inventory: If inventory drifts from the target or exceeds max limits, spreads widen and/or order sizes shrink to reduce further accumulation.
    - spread_inventory_factor and spread_pnl_factor: Adjust how strongly inventory imbalance and PnL performance influence the bot’s quoted spread.
    - size_inventory_factor and size_variance: Scale order size down when inventory is off-target, and introduce randomness to avoid being too predictable.
    - pnl_widen_threshold and widen_multiplier: If PnL falls below a certain level, the bot widens spreads dramatically to limit further downside.
    - lookback_window: Determines how often to cancel stale orders and replace them with new quotes.