from typing import Annotated

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware # help build connection with react

from sqlalchemy.orm import Session
from pydantic import BaseModel

from .database import SessionLocal, ENGINE
from . import models

app = FastAPI()

# urls that are allowed to connect with our fastapi app
origins = [
    "https://localhost:3000", # url of react app

]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class TransactionBase(BaseModel):
    id:int
    amount :float
    category :str
    description :str
    is_income :bool
    date : str

class TransactionModel(TransactionBase):
    id:int

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency Injection
db_dependency = Annotated[Session, Depends(get_db)]

models.BASE.metadata.create_all(bind=ENGINE)

@app.post(path="/transactions/", response_model=TransactionModel)
async def create_transaction(transaction:TransactionBase, db:db_dependency):
    new_transaction = models.Transaction(**transaction.model_dump())
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

@app.get(path="/transactions/", response_model=list[TransactionModel])
async def read_transactions(db: db_dependency, skip:int=0, limit:int=100):
    transactions = db.query(models.Transaction).offset(skip).limit(limit).all()
    return transactions