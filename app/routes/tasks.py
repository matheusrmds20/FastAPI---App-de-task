from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.task import TasksDB
from app.models.user import UserDB
from app.schemas.task import *
from app.schemas.user import *
from app.dependencies.auth import get_current_user
from app.services.task_service import *
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
        return TaskService.Create_task(db, user.id, task)
    
    except BadRequest as m:
        error_detail = str(m) if str(m) else "Erro ao criar task"
        raise HTTPException(status_code=400, detail=str(error_detail))


#Listar todas as Tasks, nao usar list = erro, apenas TaskResponse retorna um elemento, o que queremos aqui é uma lista de tasks
@router_task.get("/listar", response_model=list[TaskResponse])
def list_task(
    db: Session = Depends(get_db),
    user: UserDB = Depends(get_current_user),
):
    # Lista todas as tasks do usuario
    try:
        return TaskService.List_tasks(db, user.id)
    except BadRequest:
        raise HTTPException(status_code=400, detail="Erro ao listar tasks")
    

#Listar Tasks por Id
@router_task.get("/{task_id}", response_model=TaskResponse)
def get_task(
        task_id: int,
        db: Session = Depends(get_db),
        user: str =Depends(get_current_user),
):
    # Lisdta

    try:
        return TaskService.List_by_id(db, task_id, user.id)
    except BadRequest as m:
        error_detail = str(m) if str(m) else "Erro ao listar task"
        raise HTTPException(status_code=400,detail=str(error_detail))

    


#Deletar Tasks
@router_task.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
        task_id: int,
        db: Session = Depends(get_db),
        user: UserDB = Depends(get_current_user),
):

    try:
        return TaskService.Delete_task(db, task_id, user.id)
    except TaskNotFound as m:
        raise HTTPException(status_code=404, detail=str(m))


#Atualizar dados da task
@router_task.patch("/{task_id}")
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    user: UserDB = Depends(get_current_user),
):

    try:
        return TaskService.Update_task(db, task_id, user.id, task_update)
    except BadRequest as m:
        error_detail = str(m) if str(m) else "Erro ao atualizar task"
        raise HTTPException(status_code=400, detail=str(error_detail))