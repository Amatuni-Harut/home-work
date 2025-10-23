

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import date
from typing import List
import pandas as pd
import os

# ---------------- DATABASE SETUP ----------------
DATABASE_URL = "sqlite:///./Sales.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ---------------- FASTAPI APP ----------------
app = FastAPI(title="Sales Analytics API")

# ---------------- MODELS ----------------
class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    product = Column(String)
    category = Column(String)
    quantity = Column(Integer)
    price = Column(Float)
    date = Column(Date)


Base.metadata.create_all(bind=engine)

# ---------------- PYDANTIC MODELS ----------------
class SaleBase(BaseModel):
    product: str
    category: str
    quantity: int
    price: float
    date: date


class SaleCreate(SaleBase):
    pass


class SaleUpdate(SaleBase):
    pass


class SaleResponse(SaleBase):
    id: int

    class Config:
        from_attributes = True


# ---------------- UTILS ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def data_csv() -> None:

    if not os.path.exists("data_sales.csv"):
        print("data_sales.csv not found")
        return

    db: Session = next(get_db())
    try:
        if db.query(Sale).count() > 0:
            print(" Data already exists in database")
            return

        df: pd.DataFrame = pd.read_csv("data_sales.csv")
        for row in df.itertuples(index=False):
            db.add(Sale(
                product=row.product,
                category=row.category,
                quantity=int(row.quantity),
                price=float(row.price),
                date=pd.to_datetime(row.date).date()
            ))
        db.commit()
        print(" Data imported successfully")
    except:
        db.rollback()
        print(f" Error importing data:")
    finally:
        db.close()


# ---------------- ROUTES ----------------
@app.on_event("startup")
def startup_event():
    data_csv()


@app.post("/sales/", response_model=SaleResponse)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    new_sale = Sale(**sale.dict())
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    return new_sale


@app.get("/sales", response_model=List[SaleResponse])
def get_all_sales(db: Session = Depends(get_db)):
    return db.query(Sale).all()


@app.get("/sales/{sale_id}", response_model=SaleResponse)
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale


@app.put("/sales/{sale_id}", response_model=SaleResponse)
def update_sale(sale_id: int, sale: SaleUpdate, db: Session = Depends(get_db)):
    db_sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")

    for key, value in sale.dict().items():
        setattr(db_sale, key, value)

    db.commit()
    db.refresh(db_sale)
    return db_sale


@app.delete("/sales/{sale_id}")
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    db_sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")

    db.delete(db_sale)
    db.commit()
    return {"message": "Sale deleted successfully"}


@app.get("/analytics/summary")
def analytics_summary(db: Session = Depends(get_db)):
    sales = db.query(Sale).all()
    if not sales:
        return {"message": "No data"}

    df = pd.DataFrame([{
        "product": s.product,
        "category": s.category,
        "quantity": s.quantity,
        "price": s.price,
        "date": s.date,
        "revenue": s.quantity * s.price
    } for s in sales])

    return {
        "total_revenue": float(df["revenue"].sum()),
        "total_items_sold": int(df["quantity"].sum()),
        "avg_price_by_category": df.groupby("category")["price"].mean().to_dict(),
        "total_sales_by_category": df.groupby("category")["revenue"].sum().to_dict()
    }


                



