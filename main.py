from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from models import usuario
from database import Base, engine

import database
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)
class LoginRequest(BaseModel):
    name: str | None = None
    email: str
    password: str

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"hello": "world"}

@app.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(usuario).filter(usuario.email == data.email).first()
    if not user:
        return HTTPException(status_code=404, detail="User Not found")
    else:
        if data.password == user.password:
            return {"logged":True}
        else:
            return {"logged":False}


@app.post("/register")
def register(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(usuario).filter(usuario.email == data.email).first()
    if not user:
        new_user = usuario(name = data.name, email=data.email, password=data.password)
        db.add(new_user)
        db.commit()
        return new_user
    else:
        return "The email already exists"

