Finovax Backtrading, Livetrading with TraderWorkstation

1. Backtesting

1.1 Environment Set Up 
conda create -n backtest-env python=3.9
conda activate backtest-env
conda install numpy=1.26 pandas 
pip install matplotlib 
pip install yfinance
pip install backtrader

1.2 Backtesting a simple moving average with editable parameters for short and long periods

python backtesting.py

short and long periods determine how sensitive we are to price changes  
-> smaller short and long periods will make the algorithm more reactive
-> larger short and long periods will make the algorithm less reactive in the short term

2. Livetrading

2.1 Set Up
Create an Interactive Brokers paper trading account and download TraderWorkstation 

pip install ib_insync

In TraderWorkstation, select paper trading login
with paper trading account 
file -> global configuration -> api -> settings -> disable read only api, enable socket clients, check socket port number (live and paper account will have different socket ports that you can set)
make sure all farms are connected when you click DATA

2.2 Basic Integration Scripts

Checking if we can connect to the socket and also fetch current information on our stocks
python apiconnect.py
python datafetchtest.py

2.3 Live Testing

Basic Integration of SMA buy/sell check without any current position logic, posts requests to the trade logs
python fetchandtrade.py
python livetradingwithlog.py

Full Integration checking current positions to buy and sell integrated with the SMA algorithm

python main.py