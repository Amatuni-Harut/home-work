import requests
import pandas as pd
import matplotlib.pyplot as plt

url = "https://disease.sh/v3/covid-19/historical?lastdays=30"
data = requests.get(url).json()

records = []
for country_data in data:
    country = country_data["country"]
    for date, cases in country_data["timeline"]["cases"].items():
        records.append({"country": country, "date": date, "cases": cases})

df = pd.DataFrame(records)
df["date"] = pd.to_datetime(df["date"])

pivot_df = df.pivot_table(
    index='date',
    columns='country', 
    values='cases',
    fill_value=0
)
pivot_df.to_csv("pivoted_covid.csv")

top_countries = pivot_df.iloc[-1].nlargest(5).index
pivot_df[top_countries].plot(figsize=(10, 6), title="COVID-19 Cases by Country")
plt.xlabel("Date")
plt.ylabel("Total Cases")
plt.grid(True)
plt.savefig("covid_trends.png")
plt.close()

melted_df = pivot_df.reset_index().melt(
    id_vars=['date'],
    var_name='country', 
    value_name='cases'
)

melted_df['daily_change'] = melted_df.groupby('country')['cases'].diff().fillna(0)

daily_pivot = melted_df.pivot_table(
    index='date',
    columns='country',
    values='daily_change', 
    fill_value=0
)

daily_pivot[top_countries].plot(figsize=(10, 6), title="Daily COVID-19 Cases")
plt.xlabel("Date")
plt.ylabel("New Cases per Day")
plt.grid(True)
plt.savefig("covid_daily_changes.png")
plt.close()

last_7_days = melted_df[melted_df['date'] > melted_df['date'].max() - pd.Timedelta(days=7)]
top_5 = last_7_days.groupby('country')['daily_change'].sum().nlargest(5)

print("Top 5 countries with biggest increase (7 days):")
print(top_5)