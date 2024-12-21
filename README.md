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
4. Trade Execution: Matched orders execute at the best ask price (for buy orders) or best bid price (for sell orders).
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