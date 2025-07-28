# from pydantic import BaseModel
from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Base, Product, SessionLocal, engine

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

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
async def home(request: Request, db: Session = Depends(get_db)):
    products = db.scalars(select(Product)).all()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "products": products}
    )


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
