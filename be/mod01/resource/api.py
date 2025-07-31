from fastapi import  APIRouter, Body, Request, Form, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid,json
from store.app25014_professional_hub.be.mod01.resource.model import m_resource,resourceUpdate
from rubix.be.db import rubix_collecton

app25014_professional_hub_be_mod01_resource_api = APIRouter()

# CREATE
@app25014_professional_hub_be_mod01_resource_api.post("/", response_description="Create a new resource", status_code=status.HTTP_201_CREATED, response_model=m_resource)
async def create_resource(request: Request, p_resource: m_resource = Body(...)):
    resource = jsonable_encoder(p_resource)
    ses = request.headers['x-ses']          
    j_ctx = json.loads(ses)
    print('j_ctx',j_ctx)
   
    resource['org_id']=str(j_ctx['org_id'])
    resource['org_name']=str(j_ctx['org_name'])
    print('resource-2',resource)
    xc_resources = rubix_collecton(request.app.database, "resources")
    created_resource = xc_resources.create(resource)
    return created_resource


# LIST 
@app25014_professional_hub_be_mod01_resource_api.get("/", response_description="List all resource")
def list_resource(request: Request,restype:str='',org:str=''):
    qry = {}
    if restype!='':
        qry['type_id'] = restype
        
    if org!='':
        qry['org_id'] = org
    xc_resources = rubix_collecton(request.app.database, "resources")
    resources = xc_resources.find_list(qry)
    return {"resources":resources}
 

# DELETE
@app25014_professional_hub_be_mod01_resource_api.delete("/{id}", response_description="Delete a resource")
def delete_resource(id: str, request: Request, response: Response):
    xc_resources = rubix_collecton(request.app.database, "resources")
    deleted_count = xc_resources.delete(id)

    if deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"resource with ID {id} not found")

# FIND
@app25014_professional_hub_be_mod01_resource_api.get("/{id}", response_description="Get a single resource by id")
def find_resource(id: str, request: Request):
    xc_resources = rubix_collecton(request.app.database, "resources")
    resource = xc_resources.find_item(id)
    return resource

    
# UPDATE
@app25014_professional_hub_be_mod01_resource_api.post("/{id}", response_description="Update a resource", response_model=m_resource)
async def update_resource(id: str, request: Request, resource: resourceUpdate = Body(...)):
    p = await request.json()
    
    xc_resources = rubix_collecton(request.app.database, "resources")
    updated_resource = xc_resources.update(id,p)

    return updated_resource
