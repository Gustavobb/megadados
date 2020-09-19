# mock
import json
from fastapi.encoders import jsonable_encoder

with open('mock.json', 'r') as f: db = json.load(f)
#

from typing import Optional
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel

tags_metadata = [
    {
        "name": "Tasks",
        "description": "Tasks related features.",
    }
]

app = FastAPI(title = "Megadados-api", openapi_tags = tags_metadata, description="FIrst touch with FastApi")

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

@app.get("/list/", tags = ["Tasks"], response_model = dict, summary = 'List all tasks.')
def list_tasks():
    """
    List all existent tasks and their information.
    """
    return db

@app.get("/list/{done}", tags = ["Tasks"], response_model = dict, summary = 'List tasks based on status.')
def list_tasks_filter(done: bool):
    """
    List tasks based on information "done":
    - **done**: if the task is done
     - true: done tasks.
     - false: not done tasks.
    """
    return _list_tasks_logic(done)

@app.post("/add-task/", response_model = Task, tags = ["Tasks"], summary = 'Add a new task.')
def add_task(task: Task):
    """
    Create an item with all the information:

    - **name**: each tasks must have a name
    - **description**: a long description about the task
    - **done**: if the task is done
    """
    name_idx = _db_has_name(task.name)
    if name_idx != None: 
        raise HTTPException(status_code = 400, detail = {"message" : "name already exists"})

    db["tasks"].append(jsonable_encoder(task))
    _write_json()
    return task

@app.delete("/remove-task/{name}", response_model = str, tags = ["Tasks"], summary = 'Delete a task.')
def remove_task(name: str):
    """
    Delete a task based on information "name":

    - **name**: each tasks must have a name
    """
    name_idx = _db_has_name(name)
    if name_idx == None: 
        raise HTTPException(status_code = 400, detail = {"message" : "name doesn't exists"})
    else:
        del db["tasks"][name_idx]
    _write_json()
    return name

@app.put("/update-task/", response_model = Task, tags = ["Tasks"], summary = 'Update an information from task.')
def update_task(task: Task):
    """
    Update an information ("description" or "done") from a task given its name:

    - **name**: each tasks must have a name (specify the name of the task you want to update)

    You can choose which informations you want to update, exclude the ones you don't:

    - **description**: a long description about the task
    - **done**: if the task is done
    """

    name_idx = _db_has_name(task.name)
    if name_idx == None: 
        raise HTTPException(status_code = 400, detail = {"message" : "name doesn't exists"})
    
    stored_item_data = db["tasks"][name_idx]
    stored_item_model = Task(**stored_item_data)
    update_data = task.dict(exclude_unset = True)
    updated_item = stored_item_model.copy(update = update_data)
    db["tasks"][name_idx] = jsonable_encoder(updated_item)

    _write_json()
    return db["tasks"][name_idx]