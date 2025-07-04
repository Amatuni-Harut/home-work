import argparse
import requests
import json
API_URL = "https://api.coingecko.com/api/v3/coins/markets"
def crypto_data(valuta="usd"):
    try:
        params = {
            'vs_currency': valuta,
            'order': 'market_cap_desc',
            'per_page': 100,
            'page': 1,
            'sparkline': 'false'
        }
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Failed to get crypto data:", e)
        return None
def creting_crypto_info(data, Fname=None, Fprice=None):
    try:
        for coin in data:
            name = coin['name']
            symbol = coin['symbol']
            price = coin['current_price']
            market_cap = coin['market_cap']
            volume = coin['total_volume']
            price_change = coin['price_change_percentage_24h']
            if Fname and Fname.lower() not in name.lower():
                continue
            if Fprice and price < Fprice:
                continue
            print(f"Name: {name}")
            print(f"Symbol: {symbol}")
            print(f"Current Price: {price} USD")
            print(f"Market Cap: {market_cap} USD")
            print(f"Total Volume: {volume} USD")
            print(f"24h Change: {price_change}%")
            print("-" * 40)
    except Exception as e:
        print("Error showing crypto data:", e)
def main():
    parser = argparse.ArgumentParser(description="Simple Cryptocurrency Statistics Program")
    parser.add_argument('--name', help="Filter by coin name ")
    parser.add_argument('--min-price', type=float, help="Filter by minimum current price")
    args = parser.parse_args()
    data = crypto_data()
    if data:
        creting_crypto_info(data, args.name, args.min_price)
if __name__ == '__main__':
    main()
