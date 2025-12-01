from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware  #CORS

import crud
from database import engine, localSession
from schemas import UserData, UserId
from models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

#ORIGENES PERMITIDOS FRONTEND #############################
origin = [
    ##LOCAL##
    'http://localhost:3000' # damos acceso a nuestro BackEnd únicamente desde esta URL FrontEnd local
    ##DOCKER##
    #'http://172.18.0.4:3000' # UNA VEZ LOS TRES CONTENEDORES CONECTADOS DESDE NUESTRA RED DOCKER SE ASIGNA A NUESTRO BACKEND LA IP DE NUESTRO FORNTEND
    #'*' # PARA DARA ACCESO ACUALQUIR IP PUBLICA
]
app.add_middleware(
    CORSMiddleware, 
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
###########################################################

def get_db():
    db = localSession()
    try:
        yield db
    finally:
        db.close

@app.get('/')
def root():
    return "Hi my name is Dan"

@app.get('/api/users/', response_model=list[UserId])
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db=db)

@app.get('/api/users/{id:int}', response_model=UserId)
def get_user(id, db: Session = Depends(get_db)):
    user_by_id = crud.get_user_by_id(db=db, id=id)
    if user_by_id:
        return user_by_id
    raise HTTPException(status_code=404, detail="User not found")

@app.post('/api/users/', response_model=UserId)
def create_user(user: UserData, db: Session = Depends(get_db)):
    check_name = crud.get_user_by_name(db=db, name=user.name)
    if check_name:
        raise HTTPException(status_code=400, detail="User already exists")
    return crud.create_user(db=db, user=user)
