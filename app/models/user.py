from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.database import Base


#Tabela do banco de dados para usuarios
class UserDB(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password =  Column(String, nullable=False)

    tasks = relationship("TasksDB", back_populates="proprietario")
