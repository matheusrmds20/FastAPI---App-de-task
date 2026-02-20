import pytest
from app.services.exceptions import *
from app.services.task_services import TaskService
from app.models.task import TasksDB
from app.schemas.task import TaskCreate, TaskUpdate
from pytest import ExceptionInfo





def test_create_task(db_session):

    payload = TaskCreate(title="title", description="description")

    task = TaskService.create_task(
        db_session, 
        user_id=1, 
        data = payload
)

    assert task.id is not None
    assert task.title == "title"
    assert task.user_id == 1

def test_create_task_error(db_session):

    payload = TaskCreate(title=" ", description="fazer")


    with pytest.raises(BadRequest):
        TaskService.create_task(
            db_session,
            user_id=2,
            data = payload
        )

    

def test_task_not_found(db_session):
    with pytest.raises(TaskNotFound):
        TaskService.list_by_id(db_session, task_id=100, user_id=1)





def test_update_task(db_session):
    payload = TaskUpdate(title="OutroTitulo", description="OutraDescricao")

    task = TaskService.update_task(
        db_session,
        task_id=1,
        user_id=1,
        data= payload
    )

    assert task.title == "OutroTitulo"

def test_update_task_ERROR(db_session):
    payload = TaskUpdate(title="OutroTitulo", description="OutraDescricao")
    
    with pytest.raises(TaskNotFound):
        TaskService.update_task(
            db_session,
            task_id=2,
            user_id=1,
            data =payload
        )


def test_delete_task(db_session):

    task = TaskService.delete_task(
        db_session,
        task_id=1,
        user_id=1
    )
    
    assert not task



def test_create_taskHTTP(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response =  client.post(
        "/tasks", json={"title": "Ler platao", "description": "Terminar de ler essa bosta"}, headers=headers)
    assert response.status_code == 201





def test_create_task_invalid(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.post(
        "/tasks", json={"description": "apenas para teste"}, headers=headers)

    assert response.status_code == 422




def test_delete_taskHTTP(client, user_token, task_id: int = 1):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.delete(f"/tasks/{task_id}", headers=headers
    )

    assert response.status_code == 204