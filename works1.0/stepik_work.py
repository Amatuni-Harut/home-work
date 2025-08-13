"""
#2.3  exercise 1
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
md = []
class Feedback(BaseModel):
    name: str
    message: str
@app.post("/feedback")
def receive_feedback(feedback: Feedback):
    md.append(feedback.dict())
    return {"message": f"Feedback received. Thank you, {feedback.name}."}

@app.get("/feedback")
def get_all_feedback():
    return md
"""

"""
#2.3  exercise 2
from fastapi import FastAPI
from pydantic import BaseModel, Field
app = FastAPI()
md = []
FORBIDDEN_WORDS = ["редиска", "бяка", "козявка"]
class Feedback(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    message: str = Field(..., min_length=10, max_length=500)
@app.post("/feedback")
def add_feedback(feedback: Feedback):
    l_msg = feedback.message.lower()
    for word in FORBIDDEN_WORDS:
        if word in l_msg:
            return {"error": f"Message contains forbidden word: '{word}'"}
    md.append(feedback.dict())
    return {"message": f"thank you, {feedback.name}! Your feedback has been saved."}
@app.get("/feedbacks")
def get_all_feedbacks():
    return {"feedbacks": md}
"""


"""
#2.3 execise 3
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr
app = FastAPI()
md = []
FORBIDDEN_WORDS = ["редиска", "бяка", "козявка"]
class Contact(BaseModel):
    email: EmailStr
    phone: str | None = None
class Feedback(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    message: str = Field(..., min_length=10, max_length=500)
    contact: Contact
@app.post("/feedback")
def receive_feedback(feedback: Feedback, is_premium="false"):
    premium_flag = str(is_premium).lower() in ["true", "1", "yes"]
    if feedback.contact.phone is not None:
        phone = feedback.contact.phone
        if not phone.isdigit() or not (7 <= len(phone) <= 15):
            return {"error": "number your phone  not (7–15 ) degist"}
    l_msg = feedback.message.lower()
    for word in FORBIDDEN_WORDS:
        if word in l_msg:
            return {"error": f"the message contains forbidden word: '{word}'"}
    md.append(feedback.dict())
    message = f"Thank you, {feedback.name}! Your feedback has been saved."
    if premium_flag:
        message += " Your feedback will be reviewed on a priority basis."
    return {"message": message}
@app.get("/feedback")
def get_all_feedback():
    return {"feedback": md}

    """

"""
# 3.1 exercise 1
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
app = FastAPI()
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int | None = Field(None, gt=0)  
    is_subscribed: bool | None = None
@app.post("/create_user")
async def create_user(user: UserCreate):
    return user 

"""

"""
# 3.1 excersise 2
from fastapi import FastAPI
app = FastAPI()
products = [
    {"product_id": 123, "name": "Smartphone", "category": "Electronics", "price": 599.99},
    {"product_id": 456, "name": "Phone Case", "category": "Accessories", "price": 19.99},
    {"product_id": 789, "name": "Iphone", "category": "Electronics", "price": 1299.99},
    {"product_id": 101, "name": "Headphones", "category": "Accessories", "price": 99.99},
    {"product_id": 202, "name": "Smartwatch", "category": "Electronics", "price": 299.99}
]
@app.get("/product/{product_id}")
async def get_product(product_id: int):
    for product in products:
        if product["product_id"] == product_id:
            return product
    return {"error": "Product not found"}, 404
@app.get("/products/search")
async def search_products(keyword: str, category: str = None, limit: int = 10):
    result = []
    for product in products:
        if keyword.lower() in product["name"].lower():
            if category is None or product["category"].lower() == category.lower():
                result.append(product)
                if len(result) >= limit:
                    break
    return result
"""