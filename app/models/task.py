from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.db.database import Base


#Tabela do banco de dados Para as tasks
class TasksDB(Base):
    __tablename__ = "Tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    done = Column(Boolean,default=False) 
    
    user_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"),nullable=False)


    # garate que nao crie task sem "Dono"
    proprietario = relationship("UserDB", back_populates="Tasks")


    __table_args__ = (
        CheckConstraint(
            "length(trim(title)) > 0",
            name="ck_task_title_not_empty"
        ),
    )
