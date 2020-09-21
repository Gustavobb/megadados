from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

#Get /
def test_read_main_returns_not_found():
    response = client.get('/')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}

#Get tasks bool
def test_read_non_bool_task():
    response = client.get('/task?completed=a') #Not boolean on a boolean query string
    assert response.status_code == 422
    assert response.json() == {"detail":[{"loc":["query","completed"],"msg":"value could not be parsed to a boolean","type":"type_error.bool"}]}

def test_read_bool_task():
    assert client.get('/task?completed=True').status_code == 200
    assert client.get('/task?completed=False').status_code == 200


#Post tasks bool
def test_write_task():
    response = client.post(
        "/task",
        json={"description": "test",
        "completed": "a"},
    )

    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body', 'item', 'completed'], 'msg': 'value could not be parsed to a boolean', 'type': 'type_error.bool'}]}


def test_write_ok_task():
    assert client.post("/task", json={"description": "test","completed": True}).status_code == 200
    assert client.post("/task", json={}).status_code == 200
    assert client.post("/task", json={"description": "test","completed": False}).status_code == 200

#Get task by uuid
def test_read_task_non_uuid():
    response = client.get('/task/a')
    assert response.status_code == 422
    assert response.json() == {"detail":[{"loc":["path","uuid_"],"msg":"value is not a valid uuid","type":"type_error.uuid"}]}


def test_read_task_uuid():
    #Non correct uuid
    response = client.get('/task/00000000-0000-0000-0000-000000000000')
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

    #Correct uuid
    uuid = client.post("/task", json={"description": "test","completed": True}).json()
    assert client.get('/task/' + uuid).status_code == 200
    

#Put update task
def test_replace_task_non_uuid():
    response = client.put('/task/a', json={"description": "test", "completed": True})
    assert response.status_code == 422
    assert response.json() == {"detail":[{"loc":["path","uuid_"],"msg":"value is not a valid uuid","type":"type_error.uuid"}]}

def test_replace_task_uuid():
    uuid = client.post("/task", json={"description": "test","completed": True}).json()
    response = client.put('/task/'+uuid, json={"description": "test", "completed": True})
    assert response.status_code == 200

#dont put body key
#test bad boolean
# def test_replace_bad_task():
#     uuid = client.post("/task", json={"description": "test","completed": True}).json()

#     response = client.put('/task/'+uuid, json={"description": "test", "completed": "a"})
#     assert response.status_code == 422
#     assert response.json() == {'detail': [{'loc': ['body', 'item', 'completed'], 'msg': 'value could not be parsed to a boolean', 'type': 'type_error.bool'}]}


#Delete task
def test_delete_task_non_uuid():
    response = client.delete("/task/a")

    assert response.status_code == 422
    assert response.json() == {"detail":[{"loc":["path","uuid_"],"msg":"value is not a valid uuid","type":"type_error.uuid"}]}


def test_delete_task_uuid():
    uuid = client.post("/task", json={"description": "test","completed": True}).json()

    #Task exists
    assert client.delete('/task/'+uuid).status_code == 200

    #Task not found
    response = client.delete('/task/00000000-0000-0000-0000-000000000000')
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


#Alters a task
def test_patch_task_non_uuid():
    response = client.patch("/task/a", json={"description": "test","completed": True})

    assert response.status_code == 422
    assert response.json() == {"detail":[{"loc":["path","uuid_"],"msg":"value is not a valid uuid","type":"type_error.uuid"}]}


def test_patch_task_uuid():
    uuid = client.post("/task", json={"description": "test","completed": True}).json()

    #Task exists
    assert client.patch('/task/'+uuid, json={"description": "teste","completed": True}).status_code == 200

    #Task not found
    response = client.patch('/task/00000000-0000-0000-0000-000000000000', json={"description": "teste","completed": True})
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

#dont put body, key
#test bad boolean
#check uuid