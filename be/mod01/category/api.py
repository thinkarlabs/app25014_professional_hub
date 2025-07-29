from fastapi import APIRouter, Body, Request, Form, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid
import json
from store.app25014_professional_hub.be.mod01.category.models import m_category,categoryUpdate
from rubix.be.db import rubix_collecton

app25014_professional_hub_be_mod01_category_api = APIRouter()

#CREATE
@app25014_professional_hub_be_mod01_category_api.post("/", response_description="Create a new category", status_code=status.HTTP_201_CREATED, response_model=m_category)
async def create_category(request: Request, p_cat: m_category = Body(...)):
    category = jsonable_encoder(p_cat)
    xc_categories = rubix_collecton(request.app.database, "categories")
    created_category = xc_categories.create(category)
    return created_category
    
#LIST 
@app25014_professional_hub_be_mod01_category_api.get("/", response_description="List all category")
def list_category(request: Request,staff: str = ''):
    qry = {}
    if staff!='':
        qry['user_id'] = staff
    xc_categories = rubix_collecton(request.app.database, "categories")
    categories = xc_categories.find_list(qry)
    return {"categories":categories}

#DELETE
@app25014_professional_hub_be_mod01_category_api.delete("/{id}", response_description="Delete a category")
def delete_category(id: str, request: Request, response: Response):
    xc_categories = rubix_collecton(request.app.database, "categories")
    deleted_count = xc_categories.delete(id)
    if deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"category with ID {id} not found")


#FIND
@app25014_professional_hub_be_mod01_category_api.get("/{id}", response_description="Get a single category by id")
def find_category(id: str, request: Request):
    xc_categories = rubix_collecton(request.app.database, "categories")
    category = xc_categories.find_item(id)
    return category
    
#UPDATE 
@app25014_professional_hub_be_mod01_category_api.post("/{id}", response_description="Update a category",)
async def update_category(id: str, request: Request, category: categoryUpdate = Body(...)):
    p = await request.json()    
    xc_categories = rubix_collecton(request.app.database, "categories")
    updated_cat = xc_categories.update(id,p)
    return updated_cat
