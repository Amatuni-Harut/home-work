from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional,List  

app = FastAPI()

current_year = datetime.now().year

class Book(BaseModel):  
    id: int
    title: str = Field(..., min_length=3) 
    author: str
    year: int = Field(..., ge=1500, le=current_year)
    is_available: bool = True

data_books = [] 

@app.post("/books")
def create_book(book: Book):  
    data_books.append(book.dict())
    return {"msg": "book created"}
@app.post("/books/bulk/")
def create_books_bulk(books: List[Book]):
    for book in books:
        data_books.append(book.dict())
    return {"msg": f"{len(books)} books created"}  

@app.get("/books")
def get_books():
    return data_books

@app.get("/books/filtersion")  
def get_book_filter(
    author: Optional[str] = None,
    is_available: Optional[bool] = None,
    min_year: Optional[int] = None,
    max_year: Optional[int] = None,
    skip: int =0,
    limit: int =10,
    sort_by: Optional[str]="id",
    order: Optional[str]="asc"

):
    result = data_books
    if author:
        result = [el for el in result if el["author"].lower() == author.lower()]

    if is_available is not None:
        result = [el for el in result if el["is_available"] == is_available]

    if min_year is not None:
        result = [el for el in result if el["year"] >= min_year]

    if max_year is not None:
        result = [el for el in result if el["year"] <= max_year] 

    if sort_by in ["title","year","author"]:
        reverse = order == "desc"    
        result =sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    result = result[skip: skip + limit]
    return result

@app.get("/books/{book_id}")
def get_book_id(book_id: int):
    for el in data_books:
        if el["id"] == book_id:
            return el
    return {"error": "id not found"}

@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    for el in data_books:
        if el["id"] == book_id:
            el.update(book.dict())
            return {"msg": "book is updated"}
    return {"error": "book not found"}

@app.get("/books/search/")
def search_book(q: str):
    result=[el for el in data_books if q.lower() in el["title"].lower()]
    return result

@app.get("/books/stats/")
def books_stats():
    total_books=len(data_books)
    is_available_books=len([el for el in data_books if el["is_available"]])
    books_the_author={}
    for el in data_books:
        books_the_author[el["author"]] =books_the_author.get(el["author"],0)+1
    return {"total books": total_books,"is available books": is_available_books,"books the author": books_the_author }    

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for el in data_books:
        if el["id"] == book_id:
            data_books.remove(el)
            return {"msg": "book is deleted"}
    return {"error": "book not found"}

@app.delete("/books/bulk/")
def delete_books_bulk(book_ids: List[int]):
    delete_count = 0
    for book_id in book_ids:
        for el in data_books:
            if el["id"] == book_id:
                data_books.remove(el)
                delete_count += 1
                break
    return {"msg": f"{delete_count} books deleted"}