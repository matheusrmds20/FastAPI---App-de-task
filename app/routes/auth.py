from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.models.user import UserDB
from app.db.database import get_db
from app.schemas.user import Create_User
from app.core.security import verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from app.services.exceptions import *
from app.services.user_service import UserService
from app.schemas.user import *
from app.dependencies.auth import get_current_user



#Caminho para o auth
router_auth = APIRouter(prefix="/auth", tags=["Auth"])

# Registrar usuario
@router_auth.post("/register", response_model=UserRespose ,status_code=status.HTTP_201_CREATED)
def register(user: Create_User, db: Session = Depends(get_db)):

    try:
        return UserService.Register(db, user)
    except AlreadyExistError as m:
        error_detail = str(m) if str(m) else "Algo deu errado"
        raise HTTPException(status_code=400, detail=str(error_detail))
    

# Rota de login com token
@router_auth.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):


    try:
        return UserService.login(db, form_data)
    except BadRequest as m:
        raise HTTPException(status_code=400, detail=(str(m)))
    


@router_auth.post("/me")
def me(current: UserDB = Depends(get_current_user)):
    return current

