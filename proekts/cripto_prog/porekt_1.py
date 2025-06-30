import argparse
import requests
import json
def get_crypto_data(limit=5):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': limit,
        'page': 1,
        'sparkline': False
    }
    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        return res.json()
    except:
        print("Error getting data")
        return None
def filter_crypto_data(data, name_filter=None, min_value=None):
    new_list = []
    for coin in data:
        if name_filter:
            if name_filter.lower() not in coin['name'].lower():
                continue
        if min_value:
            if coin['market_cap'] < min_value:
                continue
        new_list.append(coin)
    return new_list[:5]
def display_crypto_data(data):
    if not data:
        print("No data to show")
        return
    print("-" * 80)
    print("Name  Symbol   Price(USD)   Capitalization   Volume (24h)   Change (24h)")
    print("-" * 80)
    for el in data:
        name = el['name']
        sym = el['symbol'].upper()
        price = el['current_price']
        cap = el['market_cap'] / 1e9
        vol = el['total_volume'] / 1e9
        change = el['price_change_percentage_24h']
        print(f"{name:<15} {sym:<10} ${price:<13.2f} ${cap:<17.2f} ${vol:<15.2f} {change:.2f}%")
def save_to_json(data, fname):
    try:
        with open(fname, 'w') as f:
            json.dump(data, f, indent=4)
        print("Saved to", fname)
    except:
        print("Can't save file")
def main():
    parser = argparse.ArgumentParser(description="Crypto top stats")
    parser.add_argument('--name', type=str, help="Name filter")
    parser.add_argument('--min-cap', type=float, help="Min capitalization in billion")
    parser.add_argument('--save', type=str, help="Save to file")
    parser.add_argument('--limit', type=int, default=5)
    args = parser.parse_args()
    data = get_crypto_data(args.limit)
    if not data:
        return
    min_cap = args.min_cap * 1e9 if args.min_cap else None
    result = filter_crypto_data(data, args.name, min_cap)
    display_crypto_data(result)
    if args.save:
        save_to_json(result, args.save)
if __name__ == "__main__":
    main()