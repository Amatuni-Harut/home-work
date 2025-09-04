from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, validator
from typing import List, Optional

app = FastAPI()

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
async def create_movie(movie: Movie_info):
    for el in f_db:
        if el.id == movie.id:
            raise HTTPException(status_code=400, detail="Movie id already exist")
    f_db.append(movie)
    return movie

@app.get("/movies/{m_id}", response_model=Movie_info)
def get_movie_id(m_id: int):
    for el in f_db:
        if el.id == m_id:
            return el
    raise HTTPException(status_code=404, detail="Movie not found")

@app.put("/movies/{m_id}", response_model=Movie_info)
def update_movie_info(m_id: int, movie: Movie_info):
    for idx, el in enumerate(f_db):
        if el.id == m_id:
            f_db[idx] = movie
            return movie
    raise HTTPException(status_code=404, detail="Movie id not found")

@app.delete("/movies/{m_id}")
def delete_movie(m_id: int):
    for el in f_db:
        if el.id == m_id:
            f_db.remove(el)
            return {"msg": "Movie deleted"}
    raise HTTPException(status_code=404, detail="Movie id not found")
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

@app.post("/movies/bulk/", response_model=List[Movie_info])
def create_movies_bulk(movies: List[Movie_info]):
    added_movies = []
    for movie in movies:
        if any(el.id == movie.id for el in f_db):
            continue  
        f_db.append(movie)
        added_movies.append(movie)
    return added_movies

@app.delete("/movies/bulk/")
def delete_movies_bulk(ids: List[int]):
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

@app.get("/movies/search/", response_model=List[Movie_info])
def search_movies(q: str = Query(..., min_length=1, description="Keyword to search in title or genre")):
    keyword = q.lower()
    return [m for m in f_db if keyword in m.title.lower() or keyword in m.genre.lower()]

@app.get("/movies/stats/")
def movies_stats():
    if not f_db:
        return { "total_movies": 0, "average_rating": 0, "movies_genres": {}, "newest_movie": None, "oldest_movie": None }
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
    return {  "total_movies": len(f_db),"average_rating": average_rating,"movies_genres": movies_genres,"newest_movie": newest_movie,"oldest_movie": oldest_movie
    }