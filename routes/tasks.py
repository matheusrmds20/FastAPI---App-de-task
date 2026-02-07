from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.task import TasksDB
from app.models.user import UserDB
from schemas.task import *
from schemas.user import *
from dependencies.auth import get_current_user

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

    db_task = TasksDB(
        title=task.title,
        description=task.description,
        user_id = user.id
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task) 

    return db_task

#Listar todas as Tasks, nao usar list = erro, apenas TaskResponse retorna um elemento, o que queremos aqui é uma lista de tasks
@router_task.get("/listar", response_model=list[TaskResponse])
def list_task(
    db: Session = Depends(get_db),
    user: UserDB = Depends(get_current_user),
):
    # Lista todas as tasks do usuario
    tasks = db.query(TasksDB).filter(TasksDB.user_id == user.id).all()
    
    return tasks

#Listar Tasks por Id
@router_task.get("/{task_id}", response_model=TaskResponse)
def get_task(
        task_id: int,
        db: Session = Depends(get_db),
        user: str =Depends(get_current_user),
):
    # Lisdta
    task = db.query(TasksDB).filter(
        TasksDB.id == task_id,
        TasksDB.user_id == user.id
).first()

    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    
    return task

#Deletar Tasks
@router_task.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def get_task(
        task_id: int,
        db: Session = Depends(get_db),
        user: UserDB = Depends(get_current_user),
):
    task = db.query(TasksDB).filter(
        TasksDB.id == task_id,
        TasksDB.user_id == user.id
).first()

    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    


    db.delete(task)
    db.commit()


#Atualizar dados da task
@router_task.patch("/{task_id}")
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    user: UserDB = Depends(get_current_user),
):
    task = db.query(TasksDB).filter(
        TasksDB.id == task_id,
        TasksDB.user_id == user.id                               
).first()
    
    task_update = task_update.model_dump(exclude_unset=True)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")

    if task.user_id != user:
        raise HTTPException(status_code=403, detail="acao nao autorizada")

    for field, value in task_update.items():
        setattr(task, field, value,)

    db.commit()
    db.refresh(task)

    return task