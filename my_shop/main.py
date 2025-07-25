from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

fake_db = [] #temp db switch to psql connection string later

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool

@app.get("/")
async def home():
    return({"Message": "Welcome to my online shop!"})


@app.get("/products/{product_id}")
async def read_product(product_id: int):
    return {"product_id":product_id, "product":fake_db[product_id]}

@app.post("/products")
async def create_product(product: Product):
    fake_db.append(product)
    return product

@app.get("/products/")
async def filter_products(limit: int = 10):
    return{"products": fake_db[:limit], "limit": limit}
