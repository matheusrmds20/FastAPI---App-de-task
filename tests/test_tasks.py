def test_create_task(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response =  client.post(
        "/tasks", json={"title": "Ler platao", "description": "Terminar de ler essa bosta"}, headers=headers)
    assert response.status_code == 201


def test_create_task_ivalid(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.post(
        "/tasks", json={"description": "apenas para teste"}, headers=headers)

    assert response.status_code == 422