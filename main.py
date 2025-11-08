from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.openapi.models import OAuth2
from sqlalchemy.orm import Session
from sqlalchemy import text
from models import Usuario, UserData
from database import Base, engine, get_db
from auth import get_current_user, pwd_context, create_access_token, verify_password, oauth2_scheme
from requestModels import LoginRequest, NameUpdateRequest, UserDataUpdatateRequest
 
Base.metadata.create_all(bind=engine)


app = FastAPI()

@app.get("/")
def root():
    return {"hello": "world"}

@app.get("/resetdb")
def reset_db(db: Session = Depends(get_db)):
    db.execute(text("DELETE FROM users;"))
    db.commit()
    return "db cleaned"

@app.get("/showdb")
def show_db(db: Session = Depends(get_db)):
    result : list[Usuario] = db.query(Usuario).all()
    if result:
        for i in result:
            print(i.name, i.email, i.password)
    else:
        print("There is nothing on database")

@app.get("/get-userdata")
def get_user_data(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print("GU: ", token)
    email = get_current_user(token, db)
    userdata = db.query(UserData).filter(UserData.user_email == email).first()
    return userdata

@app.get("/verify-login-status")
def verify_login_status(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    email = get_current_user(token, db)
    userdata = db.query(UserData).filter(UserData.email == email).first()
    return userdata

@app.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == data.email).first()
    print(data)
    print(user)
    if user:
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
    user = db.query(Usuario).filter(Usuario.email == data.email).first()
    print(user)
    if not user:
        new_user = Usuario(email=data.email,
                           password=pwd_context.hash(str(data.password)),
                           isNew=True)
        print("password hash: ", pwd_context.hash(data.password))
        db.add(new_user)
        db.commit()

        userdata = UserData(user_email=data.email)
        db.add(userdata)
        db.commit()

        return {"status": True}
    else:
        return {"status": False}




@app.patch("/update-userdata")
def update_userdata(data: UserDataUpdatateRequest, 
                    token: str = Depends(oauth2_scheme), 
                    db: Session = Depends(get_db)):
    email = get_current_user(token, db)
    print(email)
    userdata : UserData = db.query(UserData).filter(UserData.user_email == email).first()
    print(data)
    for k, v in data.model_dump().items():
        print(k, v)
        if v == None: continue
        userdata[k] = v
    db.commit()
    db.refresh(userdata)
    return {"status": True}

@app.patch("/update")
def update_name(data: NameUpdateRequest, token: str = Depends(oauth2_scheme), db: Session= Depends(get_db)):
    email = get_current_user(token, db)
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if user:
        user.name = data.name
        db.commit()
        db.refresh(user)

@app.patch("patch-userdata")
def patch_userdata(data: UserDataUpdatateRequest, 
                    token: str = Depends(oauth2_scheme), 
                    db: Session = Depends(get_db)):
    email = get_current_user(token, db)
    userdata = db.query(UserData).filter(UserData.email == email).first()
    for k, v in data.model_dump().items():
        if k: userdata[k] = v
    db.commit()
    db.refresh(userdata)
    return {"status": True}
    

    
    
