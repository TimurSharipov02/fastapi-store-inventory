from fastapi import FastAPI, HTTPException

app = FastAPI(title="My FastAPI Project")

items = []

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health_check():
    return {"status": "OK"}

@app.post("/items/")
async def create_item(name: str, price: float):
    item = {"id": len(items) + 1, "name": name, "price": price}
    items.append(item)
    return item

@app.get("/items/")
async def get_items():
    return items
