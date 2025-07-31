from fastapi import APIRouter, Body, Request, Form, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid
import json
from store.app25014_professional_hub.be.mod01.account.models import m_account,accountUpdate
from rubix.be.db import rubix_collecton

app25014_professional_hub_be_mod01_account_api = APIRouter()



#CREATE
@app25014_professional_hub_be_mod01_account_api.post("/", response_description="Create a new account", status_code=status.HTTP_201_CREATED, response_model=m_account)
async def create_account(request: Request, p_account: m_account = Body(...)):
    account = jsonable_encoder(p_account)
    ses = request.headers['x-ses']          
    j_ctx = json.loads(ses)
    print('j_ctx',j_ctx)
    account['org_id']=str(j_ctx['org_id'])
    account['org_name']=str(j_ctx['org_name'])
    xc_accounts = rubix_collecton(request.app.database, "accounts")
    created_account = xc_accounts.create(account)
    return created_account 
   
#LIST 
@app25014_professional_hub_be_mod01_account_api.get("/", response_description="List all account")
def list_account(request: Request, org: str = ''):
    qry = {}
    if org!='':
        qry['org_id'] = org
    xc_accounts = rubix_collecton(request.app.database, "accounts")
    accounts = xc_accounts.find_list(qry)
    return {"accounts":accounts}
 


#DELETE
@app25014_professional_hub_be_mod01_account_api.delete("/{id}", response_description="Delete a account")
def delete_account(id: str, request: Request, response: Response):
    xc_accounts = rubix_collecton(request.app.database, "accounts")
    deleted_count = xc_accounts.delete(id)
    if deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"account with ID {id} not found")


#FIND
@app25014_professional_hub_be_mod01_account_api.get("/{id}", response_description="Get a single account by id")
def find_account(id: str, request: Request):
    xc_accounts = rubix_collecton(request.app.database, "accounts")
    account = xc_accounts.find_item(id)
    return account
   
#UPDATE
@app25014_professional_hub_be_mod01_account_api.post("/{id}", response_description="Update a account", response_model=m_account)
async def update_account(id: str, request: Request, account: accountUpdate = Body(...)):
    p = await request.json()    
    xc_accounts = rubix_collecton(request.app.database, "accounts")
    updated_account = xc_accounts.update(id,p)

    return updated_account