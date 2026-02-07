from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt ,JWTError
import bcrypt
from  app.core.config import settings

# Cria o hash na senha
def hash_password(password: str) -> str:
    # Converte string para byte
    pwd_bytes = password.encode("utf-8")
    # Salt de criptografia
    salt = bcrypt.gensalt()
    # Cria o hash
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)

    return hashed_password.decode("utf-8")


# vefica se senhas sao iguais
def verify_password(password: str, hashed_password: str):

    # Compara os bytes das senhas
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


# Criacao do token de seguranca
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
   
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)



