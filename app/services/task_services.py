from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate, TaskUpdate
from sqlalchemy.exc import IntegrityError
from app.models.task import TasksDB
from app.services.exceptions import *
from sqlalchemy import func, asc, desc


class TaskService:


    @staticmethod
    def create_task(db: Session, user_id: id, data: TaskCreate):
        existing_task = db.query(TasksDB).filter(
            func.lower(TasksDB.title) == func.lower(data.title)
).first()

        if existing_task:
            raise AlreadyExistError("Task ja existente")
        
        if not data.title or data.title.strip() == "":
            raise BadRequest("Titulo precisa ter ao menos um caracter")


        try:
            task = TasksDB(
                title = data.title,
                description = data.description,
                user_id=user_id
            )

            db.add(task)
            db.commit()
            db.refresh(task)

            return task

        except IntegrityError:
            db.rollback(),
            raise ValueError("Erro ao criar task")
        

    @staticmethod
    def list_tasks(db: Session,
                   user_id: id, 
                   page: int = 1, 
                   limit: int = 5, 
                   status: str | None = None,
                   order_by: str = "created_at"
    ):
        querry = db.query(TasksDB).filter(TasksDB.user_id == user_id)

        allowerd_other_field = {"created_at", "title", "status"}
        
        # Filtro
        if status:
            querry = querry.filter(TasksDB.done == status)
        # Ordernacao
        if hasattr(TasksDB, order_by):
            querry = querry.order_by(asc(getattr(TasksDB, order_by)))
    
        #Paginacao   
        offset = (page - 1) * limit

        tasks = querry.offset(offset).limit(limit).all()

        

        if order_by not in allowerd_other_field:
            order_by = "created_at"
        
        if user_id != TasksDB.user_id:
            raise NotAuthorized()


        return tasks
    


    @staticmethod
    def list_by_id(db: Session,task_id: id ,user_id: id):
        task = db.query(TasksDB).filter(
            TasksDB.id == task_id,

).first()
        
        if not task:
            raise TaskNotFound()


        if task.user_id != user_id:
            raise NotAuthorized()



        return task
    

    @staticmethod
    def delete_task(db: Session, task_id: id, user_id: id):
        
        task_existence = db.query(TasksDB).filter(TasksDB.id == task_id).first()

        if not task_existence:
            raise TaskNotFound(task_id)




        task = TaskService.list_by_id(db, task_id, user_id)

        db.delete(task)
        db.commit()
        

    @staticmethod
    def update_task(db: Session, task_id: int, user_id: int, data: TaskUpdate):

        task = TaskService.list_by_id(db, task_id, user_id)

        
        if not task:
            raise TaskNotFound()
        





        try:
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(task, field, value)

            db.commit()
            db.refresh(task)
            return task

        except IntegrityError:
            db.rollback()
            raise ValueError("Erro ao atualizar task")
        

