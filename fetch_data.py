import requests
import time
from models import Currency, Market

currency_url = "https://bittrex.com/api/v1.1/public/getmarketsummaries"
market_url = "https://bittrex.com/api/v1.1/public/getmarkets"
# Set variables for API links.


def market_update(currency):
    market_response = requests.request("GET", market_url).json()['result']
    # Create a new variable to instantiate the api.
    isFound = False
    # crypto-currency is set to not being in the database.
    for item in market_response:
        if item["MarketName"] == currency.coin_pair:
            # if the
            isFound = True
            coin_ticker = item['MarketCurrency']
            coin_base = item['BaseCurrency']
            coin_name = item['MarketCurrencyLong']
            coin_pair = item['MarketName']
            coin_active = item['IsActive']
            coin_created = item['Created']
            coin_logo = item['LogoUrl']

            Market.create(coin_ticker=coin_ticker,
                            coin_base=coin_base,
                            coin_name=coin_name,
                            coin_pair=coin_pair,
                            coin_active=coin_active,
                            coin_created=coin_created,
                            coin_logo=coin_logo,
                            currency_id=currency.id).save()
            break
    if not isFound:
        Market.create(currency_id=currency.id).save()

def currency_update():
    while True:
        currency_response = requests.request("GET", currency_url).json()['result']
        for item in currency_response:

            coin_pair = item['MarketName']
            day_high = item['High']
            day_low = item['Low']
            volume = item['Volume']
            last_price = item['Last']
            base_volume = item['BaseVolume']
            bid_price = item['Bid']
            ask_price = item['Ask']
            open_buy = item['OpenBuyOrders']
            open_sell = item['OpenSellOrders']
            prev_day = item['PrevDay']

            currency = Currency.select().where(Currency.coin_pair == coin_pair)

            if not currency:
                Currency.create(coin_pair=coin_pair,
                                day_high=day_high,
                                day_low=day_low,
                                volume=volume,
                                last_price=last_price,
                                base_volume=base_volume,
                                bid_price=bid_price,
                                ask_price=ask_price,
                                open_buy=open_buy,
                                open_sell=open_sell,
                                prev_day=prev_day).save()

                currency = Currency.select().where(Currency.coin_pair == coin_pair).get()
                market_update(currency)

            elif currency:
                Currency.update(day_high=day_high,
                                day_low=day_low,
                                volume=volume,
                                last_price=last_price,
                                base_volume=base_volume,
                                bid_price=bid_price,
                                ask_price=ask_price,
                                open_buy=open_buy,
                                open_sell=open_sell,
                                prev_day=prev_day).where(Currency.coin_pair == coin_pair).execute()
        
        print("Paused for 900 seconds")
        time.sleep(900)

currency_update()
