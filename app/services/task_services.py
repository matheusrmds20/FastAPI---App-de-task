from sqlalchemy.orm import Session
from schemas.task import TaskCreate, TaskUpdate
from sqlalchemy.exc import IntegrityError
from models.task import TasksDB


class TaskService:


    @staticmethod
    def create_task(db: Session, user_id: id, data: TaskCreate):
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
    def list_tasks(db: Session, user_id: id):
        tasks = db.query(TasksDB).filter(
            TasksDB.user_id == user_id
).all()


        return tasks
    
    @staticmethod
    def list_by_id(db: Session,task_id: id ,user_id: id):
        task = db.query(TasksDB).filter(
            TasksDB.id == task_id,
            TasksDB.user_id == user_id
).first()


        return task
    

    @staticmethod
    def delete_task(db: Session, task_id: id, user_id: id):

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
        

