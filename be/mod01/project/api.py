from fastapi import APIRouter, Body, Request, Form, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid, json

from store.app25014_professional_hub.be.mod01.project.model import m_project,projectUpdate
from rubix.be.db import rubix_collecton

app25014_professional_hub_be_mod01_project_api = APIRouter()





#CREATE
@app25014_professional_hub_be_mod01_project_api.post("/", response_description="Create a new project", status_code=status.HTTP_201_CREATED, response_model= m_project)
async def create_project(request: Request, p_project: m_project = Body(...)):
    j_project = jsonable_encoder(p_project)
    xc_projects = rubix_collecton(request.app.database, "projects")
    created_project= xc_projects.create(j_project)
    return created_project
  
 
#LIST   
@app25014_professional_hub_be_mod01_project_api.get("/", response_description="List all projects")
def list_projects(request: Request,status:str='',staff:str=''):
    qry = {}
    
    if 'x-ses' in request.headers:
        ses = request.headers['x-ses']        
        j_ctx = json.loads(ses)
        
    if status!='':
        qry['status_id'] = status
        
    if staff!='':
        qry['user_id'] = staff
        
    xc_projects = rubix_collecton(request.app.database, "projects")
    projects = xc_projects.find_list(qry)     
    return {"projects":projects}

 
#DELETE 
@app25014_professional_hub_be_mod01_project_api.delete("/{id}", response_description="Delete a ")
def delete_project(id: str, request: Request, response: Response):    
    xc_projects = rubix_collecton(request.app.database, "projects")
    deleted_count = xc_projects.delete(id)

    if deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"project with ID {id} not found")
    
    
#FIND
@app25014_professional_hub_be_mod01_project_api.get("/{id}", response_description="Get a single project by id", response_model=m_project)
def find_project(id: str, request: Request):
    xc_projects = rubix_collecton(request.app.database, "projects")
    project = xc_projects.find_item(id)
    return project
   

# UPDATE
@app25014_professional_hub_be_mod01_project_api.post("/{id}", response_description="Update a project", response_model=m_project)
async def update_project(id: str, request: Request, p_project: projectUpdate = Body(...)):
    p = await request.json()
    xc_projects = rubix_collecton(request.app.database, "projects")
    updated_project = xc_projects.update(id,p)
    return updated_project

    
   