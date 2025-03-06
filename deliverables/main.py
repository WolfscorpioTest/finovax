import logging
import time
from datetime import datetime, timedelta
from ib_insync import *

# Setup logging
logging.basicConfig(
    filename='trade_log2.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log(msg):
    print(msg)
    logging.info(msg)

# Connect to IB paper trading account
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# List of volatile stocks to track
stocks = ['AAPL', 'NVDA', 'TSLA']
contracts = [Stock(symbol, 'SMART', 'USD') for symbol in stocks]

# Parameters
fast_sma_period = 10
slow_sma_period = 50
atr_period = 14
position_size = 10
stop_loss_pct = 0.03  # 3% stop loss
trailing_stop_pct = 0.05  # 5% trailing stop

# To track entry price and stops
trade_data = {}

def fetch_bars(contract, period):
    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr=f'{period} D',
        barSizeSetting='1 day',
        whatToShow='ADJUSTED_LAST',
        useRTH=True
    )
    return bars

def calculate_smas_and_atr(contract):
    bars = fetch_bars(contract, max(slow_sma_period, atr_period))

    if len(bars) < slow_sma_period:
        log(f"Not enough bars for SMA calculation for {contract.symbol}")
        return None, None, None

    closes = [bar.close for bar in bars]
    fast_sma = sum(closes[-fast_sma_period:]) / fast_sma_period
    slow_sma = sum(closes[-slow_sma_period:]) / slow_sma_period

    atr = sum([bar.high - bar.low for bar in bars[-atr_period:]]) / atr_period

    log(f"{contract.symbol} - Fast SMA: {fast_sma:.2f}, Slow SMA: {slow_sma:.2f}, ATR: {atr:.2f}")
    return fast_sma, slow_sma, atr

def get_position(contract):
    positions = ib.positions()
    for pos in positions:
        if pos.contract.symbol == contract.symbol:
            return pos.position  # positive for long, negative for short
    return 0

def check_and_trade(contract):
    fast_sma, slow_sma, atr = calculate_smas_and_atr(contract)
    if fast_sma is None or slow_sma is None or atr is None:
        return

    market_data = ib.reqMktData(contract)
    ib.sleep(2)  # Give time for data to populate

    price = market_data.last
    if price is None:
        log(f"{contract.symbol} - Price data not available. Skipping.")
        return

    log(f"{contract.symbol} - Current price: {price:.2f}")

    position = get_position(contract)

    # Check for buy signal (crossover up) - only if flat
    if position == 0 and fast_sma > slow_sma:
        log(f"{contract.symbol} - Buy signal triggered at {price:.2f}")
        order = MarketOrder('BUY', position_size)
        trade = ib.placeOrder(contract, order)
        trade_data[contract.symbol] = {
            'entry_price': price,
            'stop_loss': price * (1 - stop_loss_pct),
            'trailing_stop': price * (1 - trailing_stop_pct)
        }
        log(f"{contract.symbol} - BUY order placed: {trade}")

    # Check for sell signal (crossover down) - only if long
    elif position > 0 and fast_sma < slow_sma:
        log(f"{contract.symbol} - Sell signal triggered at {price:.2f}")
        order = MarketOrder('SELL', position_size)
        trade = ib.placeOrder(contract, order)
        trade_data.pop(contract.symbol, None)
        log(f"{contract.symbol} - SELL order placed: {trade}")

    # Check stop loss and trailing stop if holding position
    elif position > 0 and contract.symbol in trade_data:
        entry_price = trade_data[contract.symbol]['entry_price']
        stop_loss = trade_data[contract.symbol]['stop_loss']
        trailing_stop = trade_data[contract.symbol]['trailing_stop']

        # Update trailing stop if price rises
        if price > entry_price * (1 + trailing_stop_pct):
            new_trailing_stop = price * (1 - trailing_stop_pct)
            if new_trailing_stop > trailing_stop:
                trade_data[contract.symbol]['trailing_stop'] = new_trailing_stop
                log(f"{contract.symbol} - Updated trailing stop to {new_trailing_stop:.2f}")

        # Check if stop loss or trailing stop hit
        if price <= stop_loss:
            log(f"{contract.symbol} - Stop loss hit at {price:.2f}")
            order = MarketOrder('SELL', position_size)
            trade = ib.placeOrder(contract, order)
            trade_data.pop(contract.symbol, None)
            log(f"{contract.symbol} - SELL order placed due to stop loss: {trade}")
        elif price <= trailing_stop:
            log(f"{contract.symbol} - Trailing stop hit at {price:.2f}")
            order = MarketOrder('SELL', position_size)
            trade = ib.placeOrder(contract, order)
            trade_data.pop(contract.symbol, None)
            log(f"{contract.symbol} - SELL order placed due to trailing stop: {trade}")

# Main loop to check and trade every 5 minutes
try:
    while True:
        market_time = datetime.now().time()
        if market_time >= datetime.strptime("09:30", "%H:%M").time() and market_time <= datetime.strptime("16:00", "%H:%M").time():
            for contract in contracts:
                check_and_trade(contract)
            log("Waiting 5 minutes for next check...")
            time.sleep(300)  # 5 minutes
        else:
            log("Market closed - Sleeping for 30 minutes...")
            time.sleep(1800)  # Sleep 30 minutes during off hours
except KeyboardInterrupt:
    log("Trading session terminated by user.")
finally:
    ib.disconnect()
    log("Disconnected from IB.")
