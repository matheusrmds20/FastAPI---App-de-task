from pydantic import BaseModel, ConfigDict
from typing import Optional



class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: str |  None = None
    description: str |  None = None
    done: bool |  None = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    done: bool = False

    #torna os dados ORM em JSON
    model_config = ConfigDict(from_attributes=True)