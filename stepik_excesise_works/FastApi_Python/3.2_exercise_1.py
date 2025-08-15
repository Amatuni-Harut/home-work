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
