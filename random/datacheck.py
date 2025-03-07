from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

contract = Stock('AAPL', 'SMART', 'USD')
market_data = ib.reqMktData(contract)
ib.sleep(2)

print(f"COIN Last Price: {market_data.last}")
print(f"COIN Bid Price: {market_data.bid}")
print(f"COIN Ask Price: {market_data.ask}")

ib.disconnect()
