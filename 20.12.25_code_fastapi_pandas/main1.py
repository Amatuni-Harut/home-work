from fastapi import FastAPI, HTTPException,Query
import pandas as pd
from pydantic import BaseModel
from typing import  List, Dict

app=FastAPI()

class Sale(BaseModel):
    date: str
    product: str
    category:str
    price:float
    quantity:int
    total:float
class Summary(BaseModel):
    total_orders:int
    total_revenue:float
    average_order_value:float
        

def load_data():
    df=pd.read_csv('data.csv')
    return df

df=load_data()

df["total"]=df["price"]*df["quantity"]

@app.get("/sales", response_model=List[Sale],status_code=200)
def get_sales(category: str = None, min_total: float = None, max_total: float = None):
    result = df.copy()
    
    if category:
        result = result[result['category'] == category]
    if min_total:
        result = result[result['total'] >= min_total]
    if max_total:
        result = result[result['total'] <= max_total]
    
    if result.empty:
        raise HTTPException(status_code=404, detail="No sales found.")
    return {
        "total_orders": len(df),
        "total_revenue": float(df['total'].sum()),
        "average_order_value" : float(df['total'].mean())
    }
@app.get("/sales/summary", response_model=Summary, status_code=200)
def get_summary():
    if df.empty:
        raise HTTPException(status_code=404, detail="Нет данных")
    
    return {
        "total_orders": len(df),
        "total_revenue": float(df['total'].sum()),
        "average_order_value": float(df['total'].mean())
    }
@app.get("/sales/by-category", response_model=Dict[str, float], status_code=200)
def by_category():
    category_revenue = df.groupby('category')['total'].sum()
    if category_revenue.empty:
        raise HTTPException(status_code=404, detail="category not found")
    
    return category_revenue.to_dict()

@app.get("/sales/top-products", response_model=Dict[str, float], status_code=200)
def top_products(limit: int = Query(default=3, ge=1, le=100)):
    top = df.groupby('product')['total'].sum().sort_values(ascending=False).head(limit)

    if top.empty:
        raise HTTPException(status_code=404, detail="product not found")
    return top.to_dict()
@app.get("/sales/date-range", response_model=List[Sale], status_code=200)
def date_range(
    start_date: str = Query(..., regex=r'^\d{4}-\d{2}-\d{2}$'),
    end_date: str = Query(..., regex=r'^\d{4}-\d{2}-\d{2}$')):
    try:
        result = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        if result.empty:
            raise HTTPException(status_code=404, detail="No sales found")
        return result.to_dict(orient='records')
    except :
        raise HTTPException(status_code=400)



