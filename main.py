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

@app.get("/get-userdata")
def get_user_data(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
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
    if user:
        if verify_password(data.password, user.password):
            token = create_access_token({"email": data.email})
            return {"access_token": token}
        else:
            return {"logged": False}
    else:
        return HTTPException(status_code=404, detail="User Not found")

@app.post("/register")
def register(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == data.email).first()
    if not user:
        new_user = Usuario(email=data.email,
                           password=pwd_context.hash(str(data.password)))
        db.add(new_user)
        db.commit()

        userdata = UserData(user_email=data.email, isNew=True)
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
    userdata : UserData = db.query(UserData).filter(UserData.user_email == email).first()
    for k, v in data.model_dump().items():
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
    

    
    
