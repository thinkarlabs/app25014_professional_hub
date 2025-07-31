from fastapi import APIRouter, Body, Request, Form, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid
import json
from datetime import datetime
from store.app25014_professional_hub.be.mod01.txn.models import m_txn,txnUpdate
from store.app25014_professional_hub.be.mod01.account.models import m_account,accountUpdate
from rubix.be.db import rubix_collecton


app25014_professional_hub_be_mod01_txn_api = APIRouter()

#CREATE  
@app25014_professional_hub_be_mod01_txn_api.post("/", response_description="Create a new txn", status_code=status.HTTP_201_CREATED)
async def create_txn(request: Request, p_txn: m_txn = Body(...)):
    txn = jsonable_encoder(p_txn)
    ses = request.headers['x-ses']          
    j_ctx = json.loads(ses)
    print('j_ctx',j_ctx)
    txn['org_id']=str(j_ctx['org_id'])
    txn['org_name']=str(j_ctx['org_name'])
    xc_txns = rubix_collecton(request.app.database, "txns")
    created_txn = xc_txns.create(txn)
    
    to_acc_id = txn.get('to_acc_id')
    to_account = request.app.database["accounts"].find_one({"_id": to_acc_id})
    from_acc_id = txn.get('from_acc_id')
    from_account = request.app.database["accounts"].find_one({"_id": from_acc_id})
    if created_txn.get('txntype_name') == 'Credit':
        account_balance = to_account.get('balance', 0)
        account_balance += created_txn.get('amt')
        request.app.database["accounts"].update_one(
            {"_id": to_acc_id},
            {"$set": {"balance": account_balance}}
        )    
    if created_txn.get('txntype_name') == 'Debit':
        account_balance = from_account.get('balance', 0)
        account_balance -= created_txn.get('amt')
        request.app.database["accounts"].update_one(
            {"_id": from_acc_id},
            {"$set": {"balance": account_balance}}
        )            
    if created_txn.get('txntype_name') == 'Transfer':
        F_balance = from_account.get('balance', 0)
        F_balance -= created_txn.get('amt')
        request.app.database["accounts"].update_one(
                {"_id": from_acc_id},
                {"$set": {"balance": F_balance}}
            )
        T_balance = to_account.get('balance', 0)
        T_balance += created_txn.get('amt')
        request.app.database["accounts"].update_one(
                {"_id": to_acc_id},
                {"$set": {"balance": T_balance}}
            ) 

    to_account = request.app.database["accounts"].find_one({"_id": to_acc_id})
    from_account = request.app.database["accounts"].find_one({"_id": from_acc_id})
   

    return {"facc":from_account,"tacc":to_account,"ctxn":created_txn}


    
   
# LIST 
@app25014_professional_hub_be_mod01_txn_api.get("/", response_description="List all txn")
def list_txn(request: Request,category:str='', st: str = '', en: str = '',org: str = ''):
    qry = {}
    
    if category!='':
        qry['category_id'] = category
    if org!='':
        qry['org_id'] = org
        
    if st!='' and en!='':
        start_date = datetime.strptime(st, '%Y-%m-%d')
        end_date = datetime.strptime(en, '%Y-%m-%d')
        qry['txn_date'] = {'$gte': start_date.isoformat(), '$lte': end_date.isoformat()}
        
    xc_txns = rubix_collecton(request.app.database, "txns")
    txns = xc_txns.find_list(qry)
    return {"txns": txns}



#REVERSE TXN
@app25014_professional_hub_be_mod01_txn_api.post("/reverse/{id}", response_description="Reverse a txn")
def reverse_txn(id: str, request: Request):
    
    xc_txns = rubix_collecton(request.app.database, "txns")
    created_txn = xc_txns.find_item(id)
    
    xc_txns = rubix_collecton(request.app.database, "txns")
    xc_txns.update(id,{"txntype_name": "Reversed"})
    
    to_acc_id = created_txn.get('to_acc_id')
    to_account = request.app.database["accounts"].find_one({"_id": to_acc_id})
    from_acc_id = created_txn.get('from_acc_id')
    from_account = request.app.database["accounts"].find_one({"_id": from_acc_id})
    if created_txn.get('txntype_name') == 'Credit':
        account_balance = to_account.get('balance', 0)
        account_balance -= created_txn.get('amt')
        request.app.database["accounts"].update_one(
            {"_id": to_acc_id},
            {"$set": {"balance": account_balance}}
        )
    if created_txn.get('txntype_name') == 'Debit':
        account_balance = from_account.get('balance', 0)
        account_balance += created_txn.get('amt')
        request.app.database["accounts"].update_one(
            {"_id": from_acc_id},
            {"$set": {"balance": account_balance}}
        )
    if created_txn.get('txntype_name') == 'Transfer':
        F_balance = from_account.get('balance', 0)
        F_balance += created_txn.get('amt')
        request.app.database["accounts"].update_one(
                {"_id": from_acc_id},
                {"$set": {"balance": F_balance}}
            )
        T_balance = to_account.get('balance', 0)
        T_balance -= created_txn.get('amt')
        request.app.database["accounts"].update_one(
                {"_id": to_acc_id},
                {"$set": {"balance": T_balance}}
            )
    to_account = request.app.database["accounts"].find_one({"_id": to_acc_id})
    from_account = request.app.database["accounts"].find_one({"_id": from_acc_id})
    xc_txns = rubix_collecton(request.app.database, "txns")
    created_txn = xc_txns.find_item(id)
    return {"facc":from_account,"tacc":to_account,"ctxn":created_txn}

#FIND
@app25014_professional_hub_be_mod01_txn_api.get("/{id}", response_description="Get a single txn by id")
def find_txn(id: str, request: Request):
    xc_txns = rubix_collecton(request.app.database, "txns")
    txn = xc_txns.find_item(id)
    return txn

   

