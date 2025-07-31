from fastapi import  APIRouter, Body, Request, Form, Response, HTTPException,status
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid ,json
from store.app25014_professional_hub.be.mod01.resourcetype.model import m_resourcetype,resourcetypeUpdate
from rubix.be.db import rubix_collecton

app25014_professional_hub_be_mod01_resourcetype_api = APIRouter()

# CREATE
@app25014_professional_hub_be_mod01_resourcetype_api.post("/", response_description="Create a new resourcetype", status_code=status.HTTP_201_CREATED, response_model=m_resourcetype)
async def create_resourcetype(request: Request, p_type: m_resourcetype = Body(...)):
    resourcetype = jsonable_encoder(p_type)
    ses = request.headers['x-ses']          
    j_ctx = json.loads(ses)
    print('j_ctx',j_ctx)
    resourcetype['org_id']=str(j_ctx['org_id'])
    resourcetype['org_name']=str(j_ctx['org_name'])
    print('resourcetype-2',resourcetype)
    xc_resourcetypes = rubix_collecton(request.app.database, "resourcetypes")
    created_resourcetype = xc_resourcetypes.create(resourcetype)
    return created_resourcetype


@app25014_professional_hub_be_mod01_resourcetype_api.get("/", response_description="List all resourcetypes")
def list_resourcetypes(request: Request,org:str=''):
    qry = {}
    
    if org!='':
        qry['org_id'] = org
    xc_resourcetypes = rubix_collecton(request.app.database, "resourcetypes")
    resourcetypes =  xc_resourcetypes.find_list(qry)
    return {"resourcetypes":resourcetypes}
 

 
# DELETE
@app25014_professional_hub_be_mod01_resourcetype_api.delete("/{id}", response_description="Delete a resourcetype")
def delete_resourcetype(id: str, request: Request, response: Response):
    xc_resourcetypes = rubix_collecton(request.app.database, "resourcetypes")
    deleted_count = xc_resourcetypes.delete(id)

    if deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"resourcetype with ID {id} not found")

# FIND
@app25014_professional_hub_be_mod01_resourcetype_api.get("/{id}", response_description="Get a single resourcetype by id")
def find_resourcetype(id: str, request: Request):
    xc_resourcetypes = rubix_collecton(request.app.database, "resourcetypes")
    resourcetype = xc_resourcetypes.find_item(id)
    return resourcetype
    
# UPDATE
@app25014_professional_hub_be_mod01_resourcetype_api.post("/{id}", response_description="Update a resourcetype",)
async def update_resourcetype(id: str, request: Request, resourcetype: resourcetypeUpdate = Body(...)):
    p = await request.json()
    xc_resourcetypes = rubix_collecton(request.app.database, "resourcetypes")
    updated_resourcetype = xc_resourcetypes.update(id,p)

    return updated_resourcetype
    
   