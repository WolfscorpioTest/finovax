import logging
from datetime import datetime
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

# Define the contract
contract = Stock('AAPL', 'SMART', 'USD')

def calculate_sma(contract, period=50):
    """
    Fetches the last `period` days of historical data and calculates SMA.
    """
    log(f"Fetching {period}-day historical data for SMA calculation...")
    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr=f'{period} D',
        barSizeSetting='1 day',
        whatToShow='ADJUSTED_LAST',
        useRTH=True
    )

    if not bars:
        log("Failed to fetch historical data.")
        return None

    closes = [bar.close for bar in bars]
    sma = sum(closes) / len(closes)
    log(f"Calculated {period}-day SMA: {sma:.2f}")
    return sma

def check_and_trade():
    ib.sleep(2)  # Give market data time to populate

    # Fetch latest market data
    market_data = ib.reqMktData(contract)
    ib.sleep(2)

    price = market_data.last
    log(f"Checking current price: {price}")

    if price is None:
        log("Price data not available. Skipping this check.")
        return

    # Calculate 50-day SMA dynamically
    sma = calculate_sma(contract, period=50)
    if sma is None:
        log("SMA calculation failed. Skipping trade check.")
        return

    # Trading logic - very basic example
    if price > sma:
        log(f"Price {price} > SMA {sma:.2f}: Placing BUY order")
        order = MarketOrder('BUY', 10)
        trade = ib.placeOrder(contract, order)
        log(f"BUY Order placed: {trade}")
    elif price < sma:
        log(f"Price {price} < SMA {sma:.2f}: Placing SELL order")
        order = MarketOrder('SELL', 10)
        trade = ib.placeOrder(contract, order)
        log(f"SELL Order placed: {trade}")
    else:
        log("No trade signal triggered.")

# Run check and trade once (can be scheduled to run daily)
check_and_trade()

# Disconnect from IB
ib.disconnect()

log("Trading session completed.")
