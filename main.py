# mock
import json
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

with open('mock.json', 'r') as f: db = json.load(f)
#

from typing import Optional
from fastapi import FastAPI, Query
from pydantic import BaseModel

tags_metadata = [
    {
        "name": "list tasks",
        "description": "List tasks and filter by done parameter.",
    },
    {
        "name": "add task",
        "description": "Add task to the db",
    },
    {
        "name": "remove task",
        "description": "Remove task from db",
    },
    {
        "name": "update task",
        "description": "Update task from db",
    },
]

app = FastAPI(title = "Megadados-api", openapi_tags = tags_metadata)

def _list_tasks_logic(done: int):
    tasks = {}

    for task in db["tasks"]: 
        if task["done"] == done: tasks[len(tasks)] = task

    return tasks

def _write_json():
    with open('mock.json', 'w') as f: json.dump(db, f)

def _db_has_name(name: str):
    for idx in range(len(db["tasks"])):
        print(db["tasks"][idx])
        if db["tasks"][idx]["name"] == name: return idx
    
    return

class Task(BaseModel):
    name: str
    description: Optional[str] = None
    done: Optional[int] = None

@app.get("/")
def read_root():
    return {"Hello" : "World"}

@app.get("/list/", tags = ["list tasks"], response_model = dict)
def list_tasks():
    return db

@app.get("/list/{done}", tags = ["list tasks"], response_model = dict)
def list_tasks_filter(done: int):
    """
    Create an item with all the information:

    - **done**: if the task is done
    """
    return _list_tasks_logic(done)

@app.post("/add-task/", response_model = Task, tags = ["add task"])
def add_task(task: Task):
    """
    Create an item with all the information:

    - **name**: each tasks must have a name
    - **description**: a long description about the task
    - **done**: if the task is done
    """

    name_idx = _db_has_name(task.name)
    if name_idx != None: return JSONResponse(status_code = 400, content = {"message" : "name already exists"})

    db["tasks"].append(jsonable_encoder(task))
    _write_json()
    return task

@app.delete("/remove-task/{name}", response_model = str, tags = ["remove task"])
def remove_task(name: str):
    """
    Create an item with all the information:

    - **name**: each tasks must have a name
    """
    name_idx = _db_has_name(name)
    if name_idx == None: return JSONResponse(status_code = 400, content = {"message" : "name doesn't exists"})

    del db["tasks"][name_idx]

    _write_json()
    return name

@app.put("/update-task/", response_model = Task, tags = ["update task"])
def update_task(task: Task):
    """
    Create an item with all the information:

    - **name**: each tasks must have a name
    - **description**: a long description about the task
    - **done**: if the task is done
    """

    name_idx = _db_has_name(task.name)
    if name_idx == None: return JSONResponse(status_code = 400, content = {"message" : "name doesn't exists"})
    
    stored_item_data = db["tasks"][name_idx]
    stored_item_model = Task(**stored_item_data)
    update_data = task.dict(exclude_unset = True)
    updated_item = stored_item_model.copy(update = update_data)
    db["tasks"][name_idx] = jsonable_encoder(updated_item)

    _write_json()
    return db["tasks"][name_idx]