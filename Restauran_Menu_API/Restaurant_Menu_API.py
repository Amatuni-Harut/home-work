from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import SQLModel, Session, Field, create_engine, select
from typing import List, Optional
from pydantic import validator, BaseModel

class MenuItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True

    @validator("name")
    def validator_name(cls, v):
        if len(v) < 2:
            raise ValueError("name must be at least 2 characters")
        return v

    @validator("price")
    def validator_price(cls, v):
        if v <= 0:
            raise ValueError("price must be positive")
        return v

sqlite_file_name = "menu.db"
engine = create_engine(f"sqlite:///{sqlite_file_name}", echo=True)  

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():  
    create_db_and_tables()

@app.post("/menus/", response_model=MenuItem)
def creat_new_menu_item(menu_item: MenuItem):
    with Session(engine) as session:
        session.add(menu_item)
        session.commit()
        session.refresh(menu_item)
        return menu_item

@app.get("/menus/", response_model=List[MenuItem])
def read_menu(
    is_available: Optional[bool] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    sort_by: str = Query("id"),
    sort_order: str = Query("asc")
):
    with Session(engine) as session:
          query = select(MenuItem)
          if is_available is not None:
              query = query.where(MenuItem.is_available == is_available)
          if min_price is not None:
              query = query.where(MenuItem.price >= min_price)
          if max_price is not None:
              query = query.where(MenuItem.price <= max_price)
          if search:
             query = query.where(MenuItem.name == search)
          sort_by_column = getattr(MenuItem, sort_by)
          if sort_order == "desc":
             sort_by_column = sort_by_column.desc()
          query = query.order_by(sort_by_column)
          query = query.offset(skip).limit(limit)
          items = session.exec(query).all()
          return items


@app.get("/menus/{menu_item_id}", response_model=MenuItem) 
def read_menu_item(menu_item_id: int):
    with Session(engine) as session:
        item = session.get(MenuItem, menu_item_id)
        if not item:
            raise HTTPException(status_code=404, detail="item not found")
        return item

@app.put("/menus/{item_id}", response_model=MenuItem)  
def update_menu_item_id(item_id: int, new_id: MenuItem):
    with Session(engine) as session:
        db_item = session.get(MenuItem, item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail="item id not found")
        db_item.name = new_id.name
        db_item.description = new_id.description
        db_item.price = new_id.price 
        db_item.is_available = new_id.is_available
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item

@app.delete("/menus/{item_id}", response_model=MenuItem)
def delete_menu_item_id(item_id: int):
    with Session(engine) as session:
        item = session.get(MenuItem, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="item id not found")
        session.delete(item)
        session.commit()
        return {"msg": "item deleted"}

@app.post("/menus/bulk/", response_model=List[MenuItem])
def create_more_menu_items(items: List[MenuItem]):
    with Session(engine) as session:
        session.add_all(items)
        session.commit()
        for item in items:
            session.refresh(item)
        return items

@app.delete("/menus/bulk/", response_model=List[MenuItem])
def delete_more_menu_item(item_ids: List[int]):
    with Session(engine) as session:
        for item_id in item_ids:
            item = session.get(MenuItem, item_id)
            if item:
                session.delete(item)
        session.commit()
        return {"msg": f"items {item_ids} deleted"}

@app.get("/menu/statistics/")
def get_menu_stats():
    with Session(engine) as session:
        items = session.exec(select(MenuItem)).all()
        if not items:
            raise HTTPException(status_code=404, detail="items not found")
        total = len(items)
        available = sum(1 for item in items if item.is_available)
        average_price = sum(item.price for item in items) / total
        most_expensive_item = max(items, key=lambda x: x.price)
        cheapest_item = min(items, key=lambda x: x.price)  
        return {
            "total": total,
            "available": available,
            "average_price": average_price,
            "most_expensive_item": most_expensive_item,
            "cheapest_item": cheapest_item
        }
