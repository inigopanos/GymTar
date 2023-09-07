from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from models.jointModel import joint_data

config = dotenv_values(".env")

app = FastAPI()

collection = "Joints"

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["DB"])
    # app.database = app.mongodb_client[config("Test")]
    print('Connected to the mongoDB database')

@app.get("/")
async def root():
    collection.insert_one(joint_data)
    return {"message": "Welcome to the PyMongo tutorial!"}

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

# python -m uvicorn main:app --reload