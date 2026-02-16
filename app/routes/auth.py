from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import UserDB
from app.db.database import get_db
from app.schemas.user import Create_User
from app.core.security import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

#Caminho para o auth
router_auth = APIRouter(prefix="/auth", tags=["Auth"])

# Registrar usuario
@router_auth.post("/register", status_code=status.HTTP_201_CREATED)
def register(User: Create_User, db: Session = Depends(get_db)):
    exist = db.query(UserDB).filter(UserDB.email == User.email).first()

    if exist:
        raise HTTPException(status_code=400, detail="Email ja existente")

    db_user = UserDB(
        email=User.email,
        hashed_password= hash_password(User.password)
    )


    try:
        db.add(db_user)
        db.commit()
    except IntegrityError:
        db.rollback,
        raise HTTPException(status_code=409, detail="Email ja existente")
    
    except Exception:
        db.rollback
        raise


    db.refresh(db_user)
    return db_user

# Rota de login com token
@router_auth.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == form_data.username).first()


    # Rever esse User, parece pegar o primeiro email nao o que a gente quer


    # Validacao com o banco de dados
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

