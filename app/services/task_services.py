from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate, TaskUpdate
from sqlalchemy.exc import IntegrityError
from app.models.task import TasksDB
from app.services.exceptions import *
from sqlalchemy import func


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
    def list_tasks(db: Session, user_id: id, page: int = 1, limit: int = 5):
        offset = (page - 1) * limit


        tasks = db.query(TasksDB).filter(
            TasksDB.user_id == user_id).offset(offset).limit(limit).all()


        return tasks
    


    @staticmethod
    def list_by_id(db: Session,task_id: id ,user_id: id):
        task = db.query(TasksDB).filter(
            TasksDB.id == task_id,
            TasksDB.user_id == user_id
).first()
        
        if not task:
            raise TaskNotFound()


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
    def update_task(db: Session, task_id: id, user_id: id, data: TaskUpdate):

        task = TaskService.list_by_id(db, task_id, user_id)

        try:
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(task, field, value)

            db.commit()
            db.refresh(task)
            return task

        except IntegrityError:
            db.rollback()
            raise ValueError("Erro ao atualizar task")
        

