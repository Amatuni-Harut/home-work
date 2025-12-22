from fastapi import FastAPI
import pandas as pd

app=FastAPI()


def load_data():
    df=pd.read_csv('data.csv')
    return df

df=load_data()

df["total"]=df["price"]*df["quantity"]

@app.get("/sales")
def get_sales(category: str = None, min_total: float = None, max_total: float = None):
    result = df.copy()
    
    if category:
        result = result[result['category'] == category]
    if min_total:
        result = result[result['total'] >= min_total]
    if max_total:
        result = result[result['total'] <= max_total]
    
    return result.to_dict(orient='records')

@app.get("/sales/summary")
def get_summary():
    return{
        "total_orders": len(df),
        "total_revenue": float(df['total'].sum()),
        "average_order_value": float(df['total'].mean())   }
@app.get("/sales/by_category")
def get_by_category():
    return df.groupby("category")["total"].sum().to_dict()
@app.get("/sales/top-product")
def get_top_product(limit:int=2):
     return df.groupby('product')['total'].sum().sort_values(ascending=False).head(limit).to_dict()
@app.get("/sales/date-range")
def date_range(start_date: str, end_date: str):
    result = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    return result.to_dict(orient='records')

