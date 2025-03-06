from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

print(f"Connected: {ib.isConnected()}")

contract = Stock('AAPL', 'SMART', 'USD')
ib.qualifyContracts(contract)

ticker = ib.reqMktData(contract)
ib.sleep(2)  # Wait for data to populate

print(f"Last price: {ticker.last}")
