from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.task import TasksDB
from app.models.user import UserDB
from app.schemas.task import *
from app.schemas.user import *
from app.dependencies.auth import get_current_user
from app.services.task_services import TaskService
from app.services.exceptions import *

#Caminho para a task
router_task = APIRouter(
    prefix=("/tasks"),
    tags=["Tasks"]
)

#Criar a Task
@router_task.post("/", status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    user: UserDB = Depends(get_current_user)
):
    try:
        return TaskService.create_task(db, user.id, task)
    
    except BadRequest as M:
        raise HTTPException(status_code=400, detail=str(M))


#Listar todas as Tasks, nao usar list = erro, apenas TaskResponse retorna um elemento, o que queremos aqui é uma lista de tasks
@router_task.get("/listar", response_model=TaskResponse)
def list_task(
    page: int = 1,
    limit: int = 5,
    order_by: str = "id",
    status: str | None = None,
    db: Session = Depends(get_db),
    user: UserDB = Depends(get_current_user),
):
    try:
        return TaskService.list_tasks(
            db, 
            user.id,
            page,
            limit,
            status,
            order_by
        )
    
    except BadRequest as M:
        raise HTTPException(status_code=400, detail=str(M))
    

#Listar Tasks por Id
@router_task.get("/{task_id}", response_model=TaskResponse)
def get_task(
        task_id: int,
        db: Session = Depends(get_db),
        user: str =Depends(get_current_user),
):
    # Lista
    try:
        return TaskService.list_by_id(db, task_id, user.id)
    except TaskNotFound as M:
        raise HTTPException(status_code=404, detail=str(M))
    except NotAuthorized as M:
        raise HTTPException(status_code=403, detail=str(M))

#Deletar Tasks
@router_task.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def get_task(
        task_id: int,
        db: Session = Depends(get_db),
        user: UserDB = Depends(get_current_user),
):
    try:
        return TaskService.delete_task(db, task_id, user.id)
    except BadRequest as M:
        raise HTTPException(status_code=400, detail=str(M))
    except NotAuthorized as M:
        raise HTTPException(status_code=403, detail=str(M))
    except TaskNotFound as M:
        raise HTTPException(status_code=404, detail=str(M))

#Atualizar dados da task
@router_task.patch("/{task_id}")
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    user: UserDB = Depends(get_current_user),
):
    try:
        return TaskService.update_task(db, task_id, user.id, task_update)
    except TaskNotFound as M:
        raise HTTPException(status_code=404, detail=str(M))
    except NotAuthorized as M:
        raise HTTPException(status_code=403, detail=str(M))
    except BadRequest as M:
        raise HTTPException(status_code=400, detail=str(M))