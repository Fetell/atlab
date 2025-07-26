# from pydantic import BaseModel
from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Base, Product, SessionLocal, engine

app = FastAPI()

# class Product(BaseModel):
#     name: str
#     price: float
#     in_stock: bool

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class = HTMLResponse)
async def home():
    return """
    <html>
        <body>
            <h1 style="text-align:center;">My Online Shop</h1>
            <a style="text-align:center;" href="/docs">API Docs</a>
        </body>
    </html>
    """

@app.get("/products/{product_id}")
async def read_product(product_id: int, db: Session = Depends(get_db)):
    return db.scalars(select(Product).where(Product.id == product_id)).all()

@app.post("/products")
async def create_product(name: str, price: int, stock: int, db: Session = Depends(get_db)):
    product = Product(name=name, price=price, stock=stock)
    db.add(product)
    db.commit()
    return product

@app.get("/products/")
async def filter_products(db: Session = Depends(get_db)):
    return db.scalars(select(Product)).all()
