Step 1: Introduction and Setup
1. Introduction to Backtrader
- Install Backtrader and explore its basic functionalities.
- Study the Backtrader documentation and tutorials.
- Backtest a simple moving average crossover strategy in Backtrader using historical data.


conda create -n backtest-env python=3.9
conda activate backtest-env
conda install numpy=1.26 pandas 
pip install matplotlib 
pip install yfinance
pip install backtrader

python backtesting.py

2. Introduction to Interactive Brokers API
- Create an Interactive Brokers paper trading account (https://algotrading101.com/learn/interactive-brokers-paper-trading-demo/). Please resgiter and use a paper-trading account and DO NOT register/use a real-money account for this project since we don't want you to be involved in any potential capital-losing risks.
- Learn how to connect to the IB API and fetch account information.

pip install ib_insync
python apiconnect.py
python datafetchtest.py

with paper trading account 
file -> global configuration -> api -> settings -> disable read only api, enable socket clients, check socket port number (live and paper account will have different socket ports that you can set)
make sure all farms are connected when you click DATA 

Step 2: Developing the Trading Strategy
1. Simple Moving Average Crossover Strategy
- Understand the moving average crossover strategy: buy when the short-term moving average crosses above the long-term moving average, and sell when it crosses below.
- Implement the strategy in Backtrader and backtest it with historical data.

implemented in backtesting.py 

2. Enhancing the Strategy
- Add parameters to the strategy to make the moving average periods configurable.
- Test the strategy with different parameter values to understand its behavior.

configured 
-> smaller short and long periods will make the algorithm more reactive
-> larger short and long periods will make the algorithm less reactive in the short term

Step 3: Integration with Interactive Brokers
1. Connecting Backtrader to IB
- Set up a connection between Backtrader and the IB paper trading account.
- Modify the strategy to place real-time trades using the IB API.
- Implement a mechanism to fetch real-time daily market data from IB. Please note that we don't need intra-day minute or hourly data since they are harder to get, so daily data would be good enough. Therefore, you can build daily strategies, either by getting the data using IB's Python API, or using Yahoo Finance's Python API just in case you find it difficult to use IB's API to get live daily data.
2. Testing the Integration
- Conduct a series of tests to ensure the strategy places trades correctly in the paper trading account.
- Monitor the trades and ensure they align with the strategy’s signals.



Step 4: Live Testing and Documentation
1. Live Testing
- Run the strategy in real-time using the IB paper trading account.
- Monitor the strategy's performance and log the results.
- Make necessary adjustments based on observed performance.
