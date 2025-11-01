from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.openapi.models import OAuth2
from sqlalchemy.orm import Session
from sqlalchemy import text
from models import usuario
from database import Base, engine, get_db
from auth import get_current_user, pwd_context, create_access_token, verify_password, oauth2_scheme
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)

class LoginRequest(BaseModel):
    email: str
    password: str

class nameUpdateRequest(BaseModel):
    name: str

app = FastAPI()

@app.get("/")
def root():
    return {"hello": "world"}

@app.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(usuario).filter(usuario.email == data.email).first()
    print(data)
    print(user)
    if user:
        print("1")
        if verify_password(data.password, user.password):
            token = create_access_token(data.model_dump())
            print("TOKEN: ", token)
            return {"access_token": token}
        else:
            return {"logged": False}
    else:
        return HTTPException(status_code=404, detail="User Not found")


@app.post("/register")
def register(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(usuario).filter(usuario.email == data.email).first()
    if not user:
        new_user = usuario(email=data.email, password=pwd_context.hash(str(data.password)))
        print("password hash: ", pwd_context.hash(data.password))
        db.add(new_user)
        db.commit()
        return {"status": True}
    else:
        return "The email already exists"


@app.get("/resetdb")
def reset_db(db: Session = Depends(get_db)):
    db.execute(text("DELETE FROM users;"))
    db.commit()
    return "db cleaned"

@app.get("/showdb")
def show_db(db: Session = Depends(get_db)):
    result : list[usuario] = db.query(usuario).all()
    if result:
        for i in result:
            print(i.name, i.email, i.password)
    else:
        print("There is nothing on database")

@app.post("/update-name")
def update_name(data: nameUpdateRequest, token: str = Depends(oauth2_scheme), db: Session= Depends(get_db)):
    email = get_current_user(token, db)
    user = db.query(usuario).filter(usuario.email == email).first()
    if user:
        user.name = data.name
        db.commit()
        db.refresh(user)
    

    
    
