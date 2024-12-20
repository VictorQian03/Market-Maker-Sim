# Market-Maker-Sim
src guide:
- src/core/: Core logic for the simulation
    - order_book.py: Handles the order book data structure and operations 
    - trade.py: Represents a trade event when an order is filled
    - event.py: Base class for events in the simulation
    - time_event.py: Event class specifically for time passing
    - market.py: Simulates the market environment where trades happen
    - utils.py: Utility functions for the simulation.
- src/bots/: Contains bot implementations.
    - base_bot.py: Abstract base class for bots.
    - simple_mm_bot.py: Basic market-making bot
    - random_bot.py: Random order placement for baseline comparison.
- src/simulation/: Simulation logic and metrics.
    - simulator.py: Manages the simulation loop and time steps.
    - metrics.py: Calculates PnL, inventory, and other performance metrics.

Simulation assumptions:
- Order Matching: Orders are matched on a price-time priority. We use the ask price as the trade price. 
- Discrete Time: Simulation proceeds forward in discrete time steps.
- Mid-Price Calculation: Average of the best bid and ask. 
- Limited order book depth