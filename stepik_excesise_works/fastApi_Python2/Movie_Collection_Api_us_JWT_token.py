from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Query, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, validator
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import List, Optional

SECRET_KEY = "Supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def vwerify_password(plain_password, hashed_password):  
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

fake_user_db = {
    "User1": {
        "username": "User1",
        "hashed_password": get_password_hash("pass1"),
        "disabled": False,
    }
}

def get_user(db, username: str) -> Optional[UserInDB]:
    user = db.get(username)
    if user:
        return UserInDB(**user)
    return None

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user or not vwerify_password(password, user.hashed_password):
        return None
    return user

def crete_access_token(data: dict, expires_delta: Optional[timedelta] = None): 
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire, "sub": data.get("sub")})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,   
        detail="invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(fake_user_db, username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="user disabled")
    return current_user

app = FastAPI()


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_user_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crete_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


class Movie_info(BaseModel):
    id: int
    title: str = Field(min_length=2, description="Title must have at least 2 characters")
    genre: str = "Unknown"
    year: int = Field(gt=1888, description="Year must be after 1888")
    rating: float = Field(ge=0.0, le=10.0, description="Rating must be between 0.0 and 10.0")

    @validator("title")
    def check_title(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v

f_db: List[Movie_info] = []


@app.post("/movies", response_model=Movie_info)
async def create_movie(movie: Movie_info, current_user: UserInDB = Depends(get_current_active_user)):
    for el in f_db:
        if el.id == movie.id:
            raise HTTPException(status_code=400, detail="Movie id already exist")
    f_db.append(movie)
    return movie

@app.put("/movies/{m_id}", response_model=Movie_info)
def update_movie_info(m_id: int, movie: Movie_info, current_user: UserInDB = Depends(get_current_active_user)):
    for idx, el in enumerate(f_db):
        if el.id == m_id:
            f_db[idx] = movie
            return movie
    raise HTTPException(status_code=404, detail="Movie id not found")

@app.delete("/movies/{m_id}")
def delete_movie(m_id: int, current_user: UserInDB = Depends(get_current_active_user)):
    for el in f_db:
        if el.id == m_id:
            f_db.remove(el)
            return {"msg": "Movie deleted"}
    raise HTTPException(status_code=404, detail="Movie id not found")

@app.post("/movies/bulk/", response_model=List[Movie_info])
def create_movies_bulk(movies: List[Movie_info], current_user: UserInDB = Depends(get_current_active_user)):
    added_movies = []
    for movie in movies:
        if any(el.id == movie.id for el in f_db):
            continue  
        f_db.append(movie)
        added_movies.append(movie)
    return added_movies

@app.delete("/movies/bulk/")
def delete_movies_bulk(ids: List[int], current_user: UserInDB = Depends(get_current_active_user)):
    deleted_ids = []
    for movie_id in ids:
        for el in f_db:
            if el.id == movie_id:
                f_db.remove(el)
                deleted_ids.append(movie_id)
                break
    if not deleted_ids:
        raise HTTPException(status_code=404, detail="Movies id not found")
    return {"deleted_ids": deleted_ids}

@app.get("/movies/{m_id}", response_model=Movie_info)
def get_movie_id(m_id: int):
    for el in f_db:
        if el.id == m_id:
            return el
    raise HTTPException(status_code=404, detail="Movie not found")

@app.get("/movies", response_model=List[Movie_info])
def get_movies(
    genre: Optional[str] = Query(None, description="Filter by genre"),
    min_rating: Optional[float] = Query(None, ge=0.0, le=10.0, description="Minimum rating"),
    from_year: Optional[int] = Query(None, gt=1888, description="Start year"),
    to_year: Optional[int] = Query(None, gt=1888, description="End year"),
    skip: int = Query(0, ge=0, description="Number of movies to skip"),
    limit: int = Query(10, ge=1, description="Maximum number of movies to return"),
    sort_by: Optional[str] = Query(None, description="Sort by 'title', 'year' or 'rating'"),
    sort_order: Optional[str] = Query("asc", description="Sort order: 'asc' or 'desc'")
):
    result = f_db
    if genre:
        result = [el for el in result if el.genre.lower() == genre.lower()]
    if min_rating is not None:
        result = [el for el in result if el.rating >= min_rating]
    if from_year is not None:
        result = [el for el in result if el.year >= from_year]
    if to_year is not None:
        result = [el for el in result if el.year <= to_year]
    if sort_by:
        reverse = sort_order == "desc"
        if sort_by == "title":
            result = sorted(result, key=lambda x: x.title, reverse=reverse)
        elif sort_by == "year":
            result = sorted(result, key=lambda x: x.year, reverse=reverse)
        elif sort_by == "rating":
            result = sorted(result, key=lambda x: x.rating, reverse=reverse)
    result = result[skip: skip + limit]
    return result

@app.get("/movies/search/", response_model=List[Movie_info])
def search_movies(q: str = Query(..., min_length=1, description="Keyword to search in title or genre")):
    keyword = q.lower()
    return [m for m in f_db if keyword in m.title.lower() or keyword in m.genre.lower()]

@app.get("/movies/stats/")
def movies_stats():
    if not f_db:
        return { 
            "total_movies": 0, 
            "average_rating": 0, 
            "movies_genres": {}, 
            "newest_movie": None, 
            "oldest_movie": None 
        }
    total_rating = 0
    movies_genres = {}
    newest_movie = oldest_movie = f_db[0]
    for el in f_db:
        total_rating += el.rating
        movies_genres[el.genre] = movies_genres.get(el.genre, 0) + 1
        if el.year > newest_movie.year:
            newest_movie = el
        if el.year < oldest_movie.year:
            oldest_movie = el
    average_rating = round(total_rating / len(f_db), 2)
    return {  
        "total_movies": len(f_db),
        "average_rating": average_rating,
        "movies_genres": movies_genres,
        "newest_movie": newest_movie,
        "oldest_movie": oldest_movie
    }
