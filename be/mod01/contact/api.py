from fastapi import  APIRouter, Body, Request, Form, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid ,json
from store.app25014_professional_hub.be.mod01.contact.model import m_contact,contactUpdate
from rubix.be.db import rubix_collecton

app25014_professional_hub_be_mod01_contact_api = APIRouter()


# CREATE
@app25014_professional_hub_be_mod01_contact_api.post("/", response_description="Create a new contact", status_code=status.HTTP_201_CREATED, response_model=m_contact)
async def create_contact(request: Request, p_contact: m_contact = Body(...)):
    contact = jsonable_encoder(p_contact)
    ses = request.headers['x-ses']          
    j_ctx = json.loads(ses)
    print('j_ctx',j_ctx)
   
    contact['org_id']=str(j_ctx['org_id'])
    contact['org_name']=str(j_ctx['org_name'])
    print('contact-2',contact)
    xc_contacts = rubix_collecton(request.app.database, "contacts")
    created_contact = xc_contacts.create(contact)
    return created_contact


@app25014_professional_hub_be_mod01_contact_api.get("/", response_description="List all contact")
def list_contact(request: Request,org:str=''):
    qry = {}
       
    if org!='':
        qry['org_id'] = org
        
    
    xc_contacts = rubix_collecton(request.app.database, "contacts")
    contacts = xc_contacts.find_list(qry)
    return {"contacts":contacts}



   
# DELETE
@app25014_professional_hub_be_mod01_contact_api.delete("/{id}", response_description="Delete a contact")
def delete_contact(id: str, request: Request, response: Response):
    xc_contacts = rubix_collecton(request.app.database, "contacts")
    deleted_count = xc_contacts.delete(id)

    if deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"asset with ID {id} not found")

# FIND
@app25014_professional_hub_be_mod01_contact_api.get("/{id}", response_description="Get a single contact by id")
def find_contact(id: str, request: Request):
    xc_contacts = rubix_collecton(request.app.database, "contacts")
    contact = xc_contacts.find_item(id)
    return contact

 
# UPDATE 
@app25014_professional_hub_be_mod01_contact_api.post("/{id}", response_description="Update a contact",response_model=m_contact)
async def update_contact(id: str, request: Request, contact: contactUpdate = Body(...)):
    p = await request.json()
    xc_contacts = rubix_collecton(request.app.database, "contacts")
    updated_contact = xc_contacts.update(id,p)

    return updated_contact
    