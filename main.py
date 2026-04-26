
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Products
from database import session, engine
import database_models
from sqlalchemy.orm import Session


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_methods=["*"], allow_headers=["*"])

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome Sneha Allady"}

products = [
    Products(id=1, name="Laptop", price=999.99, description="A high-performance laptop", quantity=10),
    Products(id=2, name="Smartphone", price=499.99, description="A powerful smartphone", quantity=20),
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    count = db.query(database_models.Products).count()
    if count == 0:
        for product in products:
            db.add(database_models.Products(**product.model_dump()))
        db.commit()

init_db()

@app.get("/products/")
def get_products(db: Session = Depends(get_db)):
    return db.query(database_models.Products).all()


# @app.get("/products/{id}")
# def get_product_by_id(id: int, db: Session = Depends(get_db)):
#     db_get_pro = db.query(database_models.Products).filter(database_models.Products.id == id).first()
#     if db_get_pro is None:
#         return "Product not found"
#     return db_get_pro

@app.post("/products/")
def add_product(product: Products, db: Session = Depends(get_db)):
    db.add(database_models.Products(**product.model_dump()))
    db.commit()
    return product

@app.put("/products/{id}")
def update_product(id: int, product: Products, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Products).filter(database_models.Products.id == id).first()
    if not db_product:
        return "Product not found"
    for key, value in product.model_dump().items():
        setattr(db_product, key, value)
    db.commit()
    return "Product updated successfully"

@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Products).filter(database_models.Products.id == id).first()
    if not db_product:
        return "Product not found"
    db.delete(db_product)
    db.commit()
    return "Product deleted successfully"
