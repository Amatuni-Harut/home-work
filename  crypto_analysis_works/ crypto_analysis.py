import requests
import pandas as pd

url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 50,
    "page": 1,
    "sparkline": False,
}
response = requests.get(url, params=params)
if response.status_code == 200:
    data = response.json()
else:
    raise Exception("error", response.status_code)
df = pd.DataFrame(data)
df = df[
    [
        "id",
        "name",
        "symbol",
        "current_price",
        "market_cap",
        "price_change_percentage_24h",
        "high_24h",
        "low_24h",
    ]
]


def main():
    print(df.head())
    print("=" * 130)
    top = df.sort_values(by="market_cap", ascending=False).head(10)
    print(top)
    print("=" * 130)
    top_gainer = df.loc[df["price_change_percentage_24h"].idxmax()]
    top_loser = df.loc[df["price_change_percentage_24h"].idxmin()]
    print(
        f"\"{top_gainer['symbol']} ({top_gainer['price_change_percentage_24h']:.2f}%)\""
    )
    print("=" * 130)
    print(
        f"\"{top_loser['symbol']} ({top_loser['price_change_percentage_24h']:.2f}%)\""
    )
    print("=" * 130)
    top_50 = df.nlargest(50, "market_cap")
    average_market_cap = top_50["market_cap"].mean()
    print(f"Average Market Cap: {average_market_cap:,.2f}\n")

    print("=" * 130)

    micro_coins = df[df["current_price"] < 1]
    print("coins price less than $1", len(micro_coins))
    print(micro_coins[["name", "current_price"]])

    print("=" * 130)
    
    top20_marketCap = df.nlargest(20, "market_cap")
    top20_marketCap.to_csv("top20_cryptos.csv", index=False)
    print("Top 20 cryptos saved to top20_cryptos.csv")


if __name__ == "__main__":
    main()
