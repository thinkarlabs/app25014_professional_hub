from fastapi import APIRouter, Body, Request, Form, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import datetime as dt
import uuid, json
from datetime import datetime
from store.app25014_professional_hub.be.mod01.task.model import m_task,taskUpdate
from rubix.be.db import rubix_collecton

app25014_professional_hub_be_mod01_task_api = APIRouter()





#CREATE       
@app25014_professional_hub_be_mod01_task_api.post("/", response_description="Create a new task", status_code=status.HTTP_201_CREATED, response_model= m_task)
async def create_task(request: Request, p_task: m_task = Body(...)):
    j_task = jsonable_encoder(p_task)
    xc_tasks = rubix_collecton(request.app.database, "tasks")
    created_task= xc_tasks.create(j_task)
    return created_task
      
#LIST    
@app25014_professional_hub_be_mod01_task_api.get("/", response_description="List all tasks")
def list_tasks(request: Request, project: str = '', status: str = '', st: str = '', en: str = '', notstatus: str = '', staff: str = ''):
    qry = {}

    if project:
        qry['project_id'] = project

    if notstatus:
        qry['status_id'] = {'$ne': notstatus}

    if status:
        qry['status_id'] = {'$eq': status}
        
    if staff!='':
        qry['user_id'] = staff

    if st:
        start_date = datetime.strptime(st, '%Y-%m-%d')
        qry['reminder_date'] = {'$gte': start_date.isoformat()}


    if en:
        end_date = datetime.strptime(en, '%Y-%m-%d')
        if end_date < datetime.today():
            if 'reminder_date' not in qry:
                qry['reminder_date'] = {}
            qry['reminder_date']['$lte'] = end_date.isoformat()
        else:
            qry['reminder_date'] = {'$lte': datetime.today().isoformat()}

    print(qry)
    xc_tasks = rubix_collecton(request.app.database, "tasks")
    tasks = xc_tasks.find_list(qry)
    return {"tasks": tasks}
 

   
 #DELETE   
@app25014_professional_hub_be_mod01_task_api.delete("/{id}", response_description="Delete a task")
def delete_task(id: str, request: Request, response: Response):
    xc_tasks= rubix_collecton(request.app.database, "tasks")
    deleted_count = xc_tasks.delete(id)

    if deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"task with ID {id} not found")  
     
      
#FIND   
@app25014_professional_hub_be_mod01_task_api.get("/{id}", response_description="Get a single author by id", response_model=m_task)
def find_task(id: str, request: Request):
    xc_tasks = rubix_collecton(request.app.database, "tasks")
    task = xc_tasks.find_item(id)
    return task

       
#UPDATE 
@app25014_professional_hub_be_mod01_task_api.post("/{id}", response_description="Update a task", response_model=m_task)
async def update_task(id: str, request: Request, task: taskUpdate = Body(...)):
    task= await request.json()
    xc_tasks = rubix_collecton(request.app.database, "tasks")
    updated_task = xc_tasks.update(id,task)
    return updated_task
    
