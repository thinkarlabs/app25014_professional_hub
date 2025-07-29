from fastapi import  APIRouter, Body, Request, Form, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid
from store.app25014_professional_hub.be.mod01.asset.model import m_asset,assetUpdate
from rubix.be.db import rubix_collecton

app25014_professional_hub_be_mod01_asset_api = APIRouter()

# CREATE
@app25014_professional_hub_be_mod01_asset_api.post("/", response_description="Create a new asset", status_code=status.HTTP_201_CREATED, response_model=m_asset)
async def create_asset(request: Request, p_asset: m_asset = Body(...)):
    asset = jsonable_encoder(p_asset)
    xc_assets = rubix_collecton(request.app.database, "assets")
    created_asset = xc_assets.create(asset)
    return created_asset

# LIST 
@app25014_professional_hub_be_mod01_asset_api.get("/", response_description="List all asset")
def list_asset(request: Request,astype:str='',staff:str=''):
    qry = {}
    if astype!='':
        qry['type_id'] = astype
        
    if staff!='':
        qry['user_id'] = staff
    xc_assets = rubix_collecton(request.app.database, "assets")
    assets = xc_assets.find_list(qry)
    return {"assets":assets}
 

# DELETE
@app25014_professional_hub_be_mod01_asset_api.delete("/{id}", response_description="Delete a asset")
def delete_asset(id: str, request: Request, response: Response):
    xc_assets = rubix_collecton(request.app.database, "assets")
    deleted_count = xc_assets.delete(id)

    if deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"asset with ID {id} not found")

# FIND
@app25014_professional_hub_be_mod01_asset_api.get("/{id}", response_description="Get a single asset by id")
def find_asset(id: str, request: Request):
    xc_assets = rubix_collecton(request.app.database, "assets")
    asset = xc_assets.find_item(id)
    return asset

    
# UPDATE
@app25014_professional_hub_be_mod01_asset_api.post("/{id}", response_description="Update a asset", response_model=m_asset)
async def update_asset(id: str, request: Request, asset: assetUpdate = Body(...)):
    p = await request.json()
    
    xc_assets = rubix_collecton(request.app.database, "assets")
    updated_asset = xc_assets.update(id,p)

    return updated_asset
