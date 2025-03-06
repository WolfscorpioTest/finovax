import time
import logging
from datetime import datetime, time as dtime
import pytz
from ib_insync import *

# Setup logging
logging.basicConfig(
    filename='trade_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log(msg):
    print(msg)
    logging.info(msg)

# Connect to IB paper trading account
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# Define multiple stock contracts
symbols = ['AAPL', 'TSLA', 'NVDA', 'COIN', 'AMD']
contracts = [Stock(symbol, 'SMART', 'USD') for symbol in symbols]

def calculate_sma(contract, period=50):
    """
    Fetches the last `period` days of historical data and calculates SMA.
    """
    log(f"{contract.symbol}: Fetching {period}-day historical data for SMA calculation...")
    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr=f'{period} D',
        barSizeSetting='1 day',
        whatToShow='ADJUSTED_LAST',
        useRTH=True  # Regular trading hours only
    )

    if not bars:
        log(f"{contract.symbol}: Failed to fetch historical data.")
        return None

    closes = [bar.close for bar in bars]
    sma = sum(closes) / len(closes)
    log(f"{contract.symbol}: Calculated {period}-day SMA: {sma:.2f}")
    return sma

def check_and_trade():
    for contract in contracts:
        ib.sleep(1)  # Small pause to avoid overloading IB

        # Fetch latest market data
        market_data = ib.reqMktData(contract)
        ib.sleep(2)  # Give IB some time to respond

        price = market_data.last
        log(f"{contract.symbol}: Checking current price: {price}")

        if price is None:
            log(f"{contract.symbol}: Price data not available. Skipping.")
            continue

        # Calculate 50-day SMA dynamically
        sma = calculate_sma(contract, period=50)
        if sma is None:
            log(f"{contract.symbol}: SMA calculation failed. Skipping trade check.")
            continue

        # Trading logic - basic SMA crossover strategy
        if price > sma:
            log(f"{contract.symbol}: Price {price} > SMA {sma:.2f}: Placing BUY order")
            order = MarketOrder('BUY', 10)
            trade = ib.placeOrder(contract, order)
            log(f"{contract.symbol}: BUY Order placed: {trade}")
        elif price < sma:
            log(f"{contract.symbol}: Price {price} < SMA {sma:.2f}: Placing SELL order")
            order = MarketOrder('SELL', 10)
            trade = ib.placeOrder(contract, order)
            log(f"{contract.symbol}: SELL Order placed: {trade}")
        else:
            log(f"{contract.symbol}: No trade signal triggered.")

def is_market_open():
    """
    Check if US stock market is open (9:30 AM - 4:00 PM Eastern Time).
    """
    nyc = pytz.timezone('America/New_York')
    now = datetime.now(nyc).time()
    return dtime(9, 30) <= now <= dtime(16, 0)

try:
    while True:
        log("====== Starting new trade check cycle ======")
        if is_market_open():
            log("Market is open. Running check_and_trade()...")
            check_and_trade()
        else:
            log("Market is closed. Skipping this cycle.")
        
        log("Cycle complete. Sleeping for 5 minutes...\n")
        time.sleep(300)  # Sleep 5 minutes
except KeyboardInterrupt:
    log("Interrupted by user. Exiting and disconnecting.")
finally:
    ib.disconnect()
    log("Disconnected from IB. Trading session completed.")
