from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

responses = {
    "bool_error": {"detail":[{"loc":["query","completed"],"msg":"value could not be parsed to a boolean","type":"type_error.bool"}]},
    "bool_error_2": {'detail': [{'loc': ['body', 'item', 'completed'], 'msg': 'value could not be parsed to a boolean', 'type': 'type_error.bool'}]},
    "not_found": {'detail': 'Not Found'},
    "task_not_found": {'detail': 'Task not found'}, 
    "invalid_uuid": {"detail":[{"loc":["path","uuid_"],"msg":"value is not a valid uuid","type":"type_error.uuid"}]},
    "example_task": {"description": "test","completed": True},
    "example_task2": {"description": "test","completed": False},
    "task_new": {"description": "testnew", "completed": True},
    "example_task_invalid": {"description": "test","completed": "a"},
    "example_task_empty": {"description": "no description","completed": False}
}

def _assert(response, status_code = None, expected_body = None):
    if status_code != None: assert response.status_code == status_code
    if expected_body != None: assert response.json() == expected_body

#Get /
def test_read_main_returns_not_found():
    _assert(response = client.get('/'), status_code = 404, expected_body = responses['not_found'])

#Get tasks bool
def test_read_non_bool_task():
    _assert(response = client.get('/task?completed=a'), status_code = 422, expected_body = responses['bool_error'])

#Get tasks based on parameter 'completed'
def test_read_bool_task():
    #Add completed task to test
    resp_true = client.post("/task", json=responses['example_task']).json()
    #Add not completed task to test
    resp_false = client.post("/task", json=responses['example_task2']).json()

    #Building response based on boolean
    dict_true = dict()
    dict_false = dict()

    dict_true[resp_true] = responses['example_task']
    dict_false[resp_false] = responses['example_task2']

    #Test if getting based on boolean
    _assert(status_code = 200, response = client.get('/task?completed=True'), expected_body=dict_true)
    _assert(status_code = 200, response = client.get('/task?completed=False'), expected_body=dict_false)

#Post tasks bool
def test_write_non_task():
    _assert(response = client.post("/task", json=responses['example_task_invalid']), status_code = 422, expected_body = responses['bool_error_2'])

def test_write_task():
    #Task
    resp = client.post("/task", json=responses['example_task'])
    _assert(response = resp, status_code = 200)
    #Check if task created
    _assert(response = client.get('/task/'+ resp.json()), status_code = 200, expected_body = responses['example_task'])
    
    #Task2
    resp = client.post("/task", json={})
    _assert(response = resp, status_code = 200)
    #Check if task2 created
    _assert(response = client.get('/task/'+ resp.json()), status_code = 200, expected_body = responses['example_task_empty'])

    #Task3
    resp = client.post("/task",json=responses['example_task2'])
    _assert(response = resp, status_code = 200)
    #Check if task3 created
    _assert(response = client.get('/task/'+ resp.json()), status_code = 200, expected_body = responses['example_task2'])


#Get task by uuid
def test_read_task_non_uuid():
    _assert(response = client.get('/task/a'), status_code = 422, expected_body = responses['invalid_uuid'])

def test_read_task_uuid():
    #Not found uuid
    _assert(response = client.get('/task/00000000-0000-0000-0000-000000000000'), status_code = 404, expected_body = responses['task_not_found'])

    #Found uuid
    _uuid = client.post("/task", json=responses['example_task']).json()
    _assert(response = client.get('/task/' + _uuid), status_code = 200)

#Put update task
def test_replace_task_non_uuid():
    _assert(response = client.put('/task/a', json=responses['example_task']), status_code = 422, expected_body = responses['invalid_uuid'])

def test_replace_task_uuid():
    _uuid = client.post("/task", json=responses['example_task']).json()
    _assert(response = client.put('/task/'+ _uuid, json=responses['task_new']), status_code = 200)

    #Check if task replaced
    _assert(response = client.get('/task/'+ _uuid), status_code = 200, expected_body = responses["task_new"])

#Delete task
def test_delete_task_non_uuid():
    _assert(response = client.delete("/task/a"), status_code = 422, expected_body = responses['invalid_uuid'])

def test_delete_task_uuid():
    _uuid = client.post("/task", json=responses['example_task']).json()

    #Task exists
    _assert(response = client.delete('/task/'+ _uuid), status_code = 200)
    #Check if task was deleted
    _assert(response = client.get('/task/'+ _uuid), status_code = 404, expected_body = responses["task_not_found"])

    #Task not found
    _assert(response = client.delete('/task/00000000-0000-0000-0000-000000000000'), status_code = 404, expected_body = responses["task_not_found"])

#Alters a task
def test_patch_task_non_uuid():
    _assert(response = client.patch("/task/a", json=responses["example_task"]), status_code = 422, expected_body = responses["invalid_uuid"])

def test_patch_task_uuid():
    _uuid = client.post("/task", json=responses['example_task']).json()

    #Task exists
    _assert(response = client.patch('/task/'+ _uuid, json=responses['task_new']), status_code = 200)

    #Check if task was updated
    _assert(response = client.get('/task/'+ _uuid), expected_body = responses["task_new"])

    #Task not found
    _assert(response = client.patch('/task/00000000-0000-0000-0000-000000000000', json=responses["example_task"]), status_code = 404, expected_body = responses["task_not_found"])
