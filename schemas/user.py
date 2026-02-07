from pydantic import BaseModel, EmailStr, ConfigDict, Field


# Entrada dos dados
class Create_User(BaseModel):
    email: EmailStr
    password: str = Field(min_length=3, max_length= 71)

# Saida dos dados
class UserRespose(BaseModel):

    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)