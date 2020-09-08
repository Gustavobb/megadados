# mock
import json
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

with open('mock.json', 'r') as f: db = json.load(f)
#

from typing import Optional
from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

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

@app.get("/list/")
def list_tasks():
    return db

@app.get("/list/{status}")
def list_tasks_filter(status: int):
    return _list_tasks_logic(status)

@app.post("/add-task/", response_model = Task)
def add_task(task: Task):
    name_idx = _db_has_name(task.name)
    if name_idx != None: return JSONResponse(status_code = 400, content = {"message" : "name already exists"})

    db["tasks"].append(jsonable_encoder(task))
    _write_json()
    return task

@app.delete("/remove-task/{name}", response_model = str)
def remove_task(name: str):
    name_idx = _db_has_name(name)
    if name_idx == None: return JSONResponse(status_code = 400, content = {"message" : "name doesn't exists"})

    del db["tasks"][name_idx]

    _write_json()
    return name

@app.put("/update-task/", response_model = Task)
def update_task(task: Task):
    name_idx = _db_has_name(task.name)
    if name_idx == None: return JSONResponse(status_code = 400, content = {"message" : "name doesn't exists"})
    
    stored_item_data = db["tasks"][name_idx]
    stored_item_model = Task(**stored_item_data)
    update_data = task.dict(exclude_unset = True)
    updated_item = stored_item_model.copy(update = update_data)
    db["tasks"][name_idx] = jsonable_encoder(updated_item)

    _write_json()
    return db["tasks"][name_idx]