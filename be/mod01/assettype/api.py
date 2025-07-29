from fastapi import  APIRouter, Body, Request, Form, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid
from store.app25014_professional_hub.be.mod01.assettype.model import m_assettype,assettypeUpdate
from rubix.be.db import rubix_collecton

app25014_professional_hub_be_mod01_assettype_api = APIRouter()

# CREATE
@app25014_professional_hub_be_mod01_assettype_api.post("/", response_description="Create a new assettype", status_code=status.HTTP_201_CREATED, response_model=m_assettype)
async def create_assettype(request: Request, p_type: m_assettype = Body(...)):
    assettype = jsonable_encoder(p_type)
    xc_assettypes = rubix_collecton(request.app.database, "assettypes")
    created_assettype = xc_assettypes.create(assettype)
    return created_assettype


@app25014_professional_hub_be_mod01_assettype_api.get("/", response_description="List all assettypes")
def list_assettypes(request: Request,staff:str=''):
    qry = {}
    
    if staff!='':
        qry['user_id'] = staff
    xc_assettypes = rubix_collecton(request.app.database, "assettypes")
    assettypes =  xc_assettypes.find_list(qry)
    return {"assettypes":assettypes}
 

 
# DELETE
@app25014_professional_hub_be_mod01_assettype_api.delete("/{id}", response_description="Delete a assettype")
def delete_assettype(id: str, request: Request, response: Response):
    xc_assettypes = rubix_collecton(request.app.database, "assettypes")
    deleted_count = xc_assettypes.delete(id)

    if deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"assettype with ID {id} not found")

# FIND
@app25014_professional_hub_be_mod01_assettype_api.get("/{id}", response_description="Get a single assettype by id")
def find_assettype(id: str, request: Request):
    xc_assettypes = rubix_collecton(request.app.database, "assettypes")
    assettype = xc_assettypes.find_item(id)
    return assettype
    
# UPDATE
@app25014_professional_hub_be_mod01_assettype_api.post("/{id}", response_description="Update a assettype",)
async def update_assettype(id: str, request: Request, assettype: assettypeUpdate = Body(...)):
    p = await request.json()
    xc_assettypes = rubix_collecton(request.app.database, "assettypes")
    updated_assettype = xc_assettypes.update(id,p)

    return updated_assettype
    
   