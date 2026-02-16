from app.models.task import *
from app.schemas.task import TaskCreate, TaskUpdate
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from .exceptions import *




class TaskService:
    pass


    @staticmethod
    def Create_task(db: Session, user_id: int, data: TaskCreate):

        task_alredy_existing = db.query(TasksDB).filter(
        func.lower(TasksDB.title) == func.lower(data.title), 
        TasksDB.user_id == user_id
).first()

        
        if task_alredy_existing:
            raise BadRequest("Task ja existente")

        try:
            task = TasksDB(
                title= data.title,
                description=data.description,
                user_id=user_id
            )

            db.add(task)
            db.commit()
            db.refresh(task)

            return task
        
        except IntegrityError:
            db.rollback()
            raise ValueError("Algo deu errado ao criar a task")






    @staticmethod
    def List_tasks(db: Session, user_id: int):
        task = db.query(TasksDB).filter( 
            TasksDB.user_id == user_id).all()
        
    
        return task


    
    @staticmethod
    def List_by_id(db: Session, task_id: int, user_id: int):
        task = db.query(TasksDB).filter(
            TasksDB.id == task_id, 
            TasksDB.user_id == user_id
).first()
        
        if not task:
            raise TaskNotFound("Task nao encontrada")
        


        return task
    


    @staticmethod
    def Update_task(db: Session, task_id: int, user_id: int, data: TaskUpdate):
        task = TaskService.List_by_id(db, task_id, user_id)

        if not task:
            raise TaskNotFound()

        if task.user_id != user_id:
            raise NotAuthorized()

        try:
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(task, field, value)

            db.commit()
            db.refresh(task)
            return task

        except IntegrityError:
            db.rollback()
            raise ValueError("Erro ao atualizar task")



    @staticmethod
    def Delete_task(db: Session, task_id: int, user_id: int):
        task = TaskService.List_by_id(db, task_id, user_id)

        if not task:
            raise TaskNotFound("Task nao encotrada")

        db.delete(task)
        db.commit()