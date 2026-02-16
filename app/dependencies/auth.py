from sqlalchemy.orm import Session
from app.db.database import get_db
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.config import settings
from app.models.user import UserDB


# Continuar com usuario logado se token valido

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print(payload)
        user_id: str = payload.get("sub")
        

        # valida token
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token Invalido")
        
    except JWTError:
        raise HTTPException(status_code=401)
        

    user = db.query(UserDB).filter(UserDB.id == int(user_id)).first()

    # validar usuario
    if not user:
            raise HTTPException(status_code=401, detail="Usuario invalido")


    return user
