from fastapi import FastAPI
from app.routers import users,item_template,auth
from app.database import engine,Base
from app import models

app = FastAPI()

app.include_router(users.router)
app.include_router(item_template.router)
app.include_router(auth.router)

@app.get("/")   #When someone sends a GET request to the / path, call the function right below this line.
def read_root(): 
    return {"message": "Hello, Farmware backend is running."}


Base.metadata.create_all(bind=engine)