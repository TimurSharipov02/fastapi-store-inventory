from fastapi import FastAPI, HTTPException
from app.database import get_db_connection, create_tables
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Store Inventory API")

# Модели данных
class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int
    category: str

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    category: str

@app.on_event("startup")
async def startup():
    await create_tables()

# Эндпоинты
@app.post("/products/", response_model=ProductResponse)
async def create_product(product: ProductCreate):
    conn = await get_db_connection()
    try:
        product_id = await conn.fetchval(
            """INSERT INTO products (name, price, quantity, category) 
               VALUES ($1, $2, $3, $4) RETURNING id""",
            product.name, product.price, product.quantity, product.category
        )
        return {**product.dict(), "id": product_id}
    finally:
        await conn.close()

@app.get("/products/", response_model=List[ProductResponse])
async def get_products(category: Optional[str] = None):
    conn = await get_db_connection()
    try:
        if category:
            products = await conn.fetch(
                "SELECT id, name, price, quantity, category FROM products WHERE category = $1",
                category
            )
        else:
            products = await conn.fetch(
                "SELECT id, name, price, quantity, category FROM products"
            )
        return [dict(product) for product in products]
    finally:
        await conn.close()

@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    conn = await get_db_connection()
    try:
        product = await conn.fetchrow(
            "SELECT id, name, price, quantity, category FROM products WHERE id = $1",
            product_id
        )
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return dict(product)
    finally:
        await conn.close()

@app.get("/stats/")
async def get_stats():
    conn = await get_db_connection()
    try:
        total_products = await conn.fetchval("SELECT COUNT(*) FROM products")
        total_value = await conn.fetchval("SELECT COALESCE(SUM(price * quantity), 0) FROM products")
        categories = await conn.fetch("SELECT category, COUNT(*) as count FROM products GROUP BY category")
        
        return {
            "total_products": total_products,
            "total_inventory_value": total_value,
            "categories": [dict(cat) for cat in categories]
        }
    finally:
        await conn.close()

@app.get("/")
async def root():
    return {"message": "Store Inventory API"}

@app.get("/health")
async def health_check():
    return {"status": "OK"}
