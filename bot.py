import cbpro
import constants
import time

BUY = 'buy'
SELL = 'sell'
class TradingSystems:
    def __init__(self, cb_pro_client):
        self.client = cb_pro_client

    def trade(self, action, limitPrice, quantity):
        if action ==BUY:
            response = self.client.buy(price = limitPrice,
            size= self.round(quantity * .99),
            order_type = 'limit',
            product_id = 'BTC-USD',
            overdraft_enabled = False)
        if action ==SELL:
            response = self.client.sell(price = limitPrice,
            size= quantity,
            order_type = 'limit',
            product_id = 'BTC-USD',
            overdraft_enabled = False)
        print(response)

    def viewAccount(self, accountCurrency):
        accounts = self.client.get_accounts()
        account = list(filter(lambda x: x['currency'] == accountCurrency, accounts))[0]
        return account

    def viewOrder(self, order_id):
        return self.client.get_order(order_id)

    def gettingCurrentPriceOfBitcoin(self):
        tick = self.client.get_product_ticker(product_id ='BTC-USD')
        return tick['bid']

    def round(self, val):
        newval = int(val* (10000000))/(10000000)
        return newval



if __name__ == "__main__":
    auth_client = cbpro.AuthenticatedClient(constants.public,
        constants.secret,
        constants.passphrase,
        api_url="https://api-public.sandbox.pro.coinbase.com")
    tradingSystems = TradingSystems(auth_client)

    currentPrice = float(tradingSystems.gettingCurrentPriceOfBitcoin())
    usdBalance = float(tradingSystems.viewAccount('USD')['balance'])

    tradingSystems.trade(BUY, currentPrice, usdBalance/currentPrice)

    # lastOrderInfo = tradingSystems.viewOrder('86488b65-0439-4641-969d-f95077b34585')
    # print(lastOrderInfo)
