from pydantic import BaseModel, ConfigDict, Field
from typing import Optional




class TaskBase(BaseModel):
    title: str = Field(min_length=1)
    description: Optional[str] = None


class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None



class TaskItemsResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    done: bool


    model_config = ConfigDict(from_attributes=True)

class TaskResponse(BaseModel):
    items: list[TaskItemsResponse]
    page: int
    limit: int

    #torna os dados ORM em JSON
    model_config = ConfigDict(from_attributes=True)