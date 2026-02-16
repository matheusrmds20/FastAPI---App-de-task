from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.user import Create_User
from app.models.user import UserDB
from .exceptions import *
from app.core.security import *


class UserService:


    @staticmethod
    def Register(db: Session, data: Create_User):
        exist = db.query(UserDB).filter(UserDB.email == data.email).first()

        if exist:
            raise AlreadyExistError("Email ja ultilizado")

        user = UserDB(
            email=data.email,
            hashed_password=hash_password(data.password)
        )

        try:
            db.add(user)
            db.commit()
            db.refresh(user)
        except IntegrityError:
            db.rollback()
            raise BadRequest()

        return user
    


    @staticmethod
    def login(db: Session, form_data: OAuth2PasswordRequestForm):
        user = db.query(UserDB).filter(UserDB.email == form_data.username).first()

        # Validacao com o banco de dados
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise BadRequest("Senha ou email invalido")
        
        
        token = create_access_token({"sub": str(user.id)})
        return {"access_token":token, "token_type": "bearer"}
    
    

    
