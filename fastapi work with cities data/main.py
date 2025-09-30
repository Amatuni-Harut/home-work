import os
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

app = FastAPI()

# -------SQLAlchemy-------
DATABASE_URL = "sqlite:///data_cities.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class City(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True, index=True)
    city_name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    population = Column(String, nullable=False)
    latitude = Column(String, nullable=False)
    longitude = Column(String, nullable=False)
    continent = Column(String, nullable=False)


Base.metadata.create_all(bind=engine)


# ---------- Pydantic ----------
class CitySchema(BaseModel):
    city_name: str
    country: str
    population: str
    latitude: str
    longitude: str
    continent: str

    class Config:
        orm_mode = True


class CityResponse(CitySchema):
    id: int


# -------- DB utils ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def read_file(db: Session, f_name):
    cities = db.query(City).all()
    with open(f_name, "w") as f:
        for el in cities:
            f.write(
                f"{el.city_name},{el.country},{el.population},{el.latitude},{el.longitude},{el.continent}\n"
            )


def start_db():
    db = SessionLocal()
    try:
        if os.path.exists("data.txt"):
            with open("data.txt", "r") as f:
                for line in f:
                    el = line.strip().split(",")
                    if len(el) == 6:
                        if_true = (
                            db.query(City)
                            .filter(City.city_name == el[0], City.country == el[1])
                            .first()
                        )
                        if not if_true:
                            city = City(
                                city_name=el[0],
                                country=el[1],
                                population=el[2],
                                latitude=el[3],
                                longitude=el[4],
                                continent=el[5],
                            )
                            db.add(city)
            db.commit()
            print("data is loaded")
        else:
            print("data.txt not found ")
    finally:
        db.close()


@app.on_event("startup")
def startup_event():
    start_db()


# ------- Fastapi-----------------
@app.get("/all_cities")
def get_all_cities(db: Session = Depends(get_db)):
    return db.query(City).all()


@app.get("/city/{c_id}")
def get_city_by_id(c_id: int, db: Session = Depends(get_db)):
    city = db.query(City).filter(City.id == c_id).first()
    if city:
        return city
    return {"error": "City not found"}


@app.post("/city")
def create_city_data(city: CitySchema, db: Session = Depends(get_db)):
    new_city = City(**city.dict())
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    read_file(db, "data.txt")
    return {"msg": "city data was created"}


@app.put("/city/{city_id}")
def update_city_data(city_id: int, city: CitySchema, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        return {"error": "City id not found"}
    city_db.city_name = city.city_name
    city_db.country = city.country
    city_db.population = city.population
    city_db.latitude = city.latitude
    city_db.longitude = city.longitude
    city_db.continent = city.continent
    db.commit()
    db.refresh(city_db)
    read_file(db, "data.txt")
    return {"msg": "city data was updated"}


@app.delete("/city/{city_id}")
def delete_city_data(city_id: int, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        return {"error": "City id not found"}
    db.delete(city_db)
    db.commit()
    read_file(db, "data.txt")
    return {"msg": "city data was deleted"}
