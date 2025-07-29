import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from dotenv import dotenv_values
from pymongo import MongoClient
from datetime import datetime
from space.app00_neev.be.main.app import app as base_app
from store.app24005_personal_hub.be.main.app import app


config = dotenv_values(".env")
app.database = app.mongodb_client[app.dbname + "_test"]
base_app.database = base_app.mongodb_client[base_app.dbname + "_test"]



#TEST CASE FOR CREATE
def test_create_txn_credit(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            new_account_response = client.post("/api/app24005_personal_hub/be/mod01/accoutn/", json={"user_id":"123","user_name":"guguldash","acc_title":"ICICI", "acc_type_name": "Bank", "acc_type_id": "Bank", "balance": 1000.00})
            new_account = new_account_response.json()
            
            new_category_response = client.post("/api/app24005_personal_hub/be/mod01/category/", json={"user_id":"123","user_name":"guguldash","name":"Salary"})
            new_category = new_category_response.json()
            
            response = client.post("/api/app24005_personal_hub/be/mod01/txn/", json={"user_id":"123","user_name":"guguldash","txn_title":"Salary Received", "txntype_name":"Credit", "txntype_id":"C", "from_acc_name":"", "from_acc_id":"", "to_acc_name":"ICICI", "to_acc_id":new_account["_id"], "amt":20000.00, "category_name":"Salary", "category_id":new_category["_id"], "txn_date": "2024-04-09"})
            assert response.status_code == 201
            body = response.json()
            if body.get("tacc") is not None:
                assert body["tacc"]["balance"] == 21000.00  
#TEST CASE FOR DEBIT
def test_create_txn_debit(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            new_account_response = client.post("/api/app24005_personal_hub/be/mod01/accoutn/", json={"user_id":"123","user_name":"guguldash","acc_title":"ICICI", "acc_type_name": "Bank", "acc_type_id": "Bank", "balance": 1000.00})
            new_account = new_account_response.json()
            
            new_category_response = client.post("/api/app24005_personal_hub/be/mod01/category/", json={"user_id":"123","user_name":"guguldash","name":"Salary"})
            new_category = new_category_response.json()
            
            response = client.post("/api/app24005_personal_hub/be/mod01/txn/", json={"user_id":"123","user_name":"guguldash","txn_title":"Salary Received", "txntype_name":"Credit", "txntype_id":"C", "from_acc_name":"", "from_acc_id":"", "to_acc_name":"ICICI", "to_acc_id":new_account["_id"], "amt":20000.00, "category_name":"Salary", "category_id":new_category["_id"], "txn_date": "2024-04-09"})
            assert response.status_code == 201
            body = response.json()
            if body.get("facc") is not None:
                assert body["facc"]["balance"] == 4700.00  
                
                
                
          
#TEST CASE FOR TRANSFER
def test_create_txn_Transfer(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            new_account_response = client.post("/api/app24005_personal_hub/be/mod01/accoutn/", json={"user_id":"123","user_name":"guguldash","acc_title":"Piggy Bank", "acc_type_name": "Bank", "acc_type_id": "Bank", "balance": 2000.00})
            new_account1 = new_account_response.json()

            new_account= client.post("/api/app24005_personal_hub/be/mod01/accoutn/", json={"user_id":"123","user_name":"guguldash","acc_title":"SBI", "acc_type_name": "Bank", "acc_type_id": "Bank", "balance": 5000.00})

            new_account2 = new_account.json()

            new_category_response = client.post("/api/app24005_personal_hub/be/mod01/category/", json={"user_id":"123","user_name":"guguldash","name":"Transfer"})
            new_category = new_category_response.json()

            response = client.post("/api/app24005_personal_hub/be/mod01/txn/", json={"user_id":"123","user_name":"guguldash","txn_title":"Purchased Grocery", "txntype_name":"Transfer", "txntype_id":"T", "from_acc_name":"Piggy Bank", "from_acc_id":new_account1["_id"], "to_acc_name":"SBI", "to_acc_id":new_account2["_id"], "amt":100.00, "category_name":"Transfer", "category_id":new_category["_id"], "txn_date": "2024-06-09"})
            assert response.status_code == 201
            body = response.json()
            if body.get("facc") is not None:
                assert body["facc"]["balance"] == 1900.00

            if body.get("tacc") is not None:
                assert body["tacc"]["balance"] == 5100.00



def test_reverse_txn_credit(capsys):
    with TestClient(app) as client:
        with capsys.disabled():

            # Create a new account
            new_account_response = client.post("/api/app24005_personal_hub/be/mod01/accoutn/", json={"user_id":"123","user_name":"guguldash","acc_title": "ICICI", "acc_type_name": "Bank", "acc_type_id": "Bank", "balance": 1000.00})
            new_account = new_account_response.json() 

            # Create a new category
            new_category_response = client.post("/api/app24005_personal_hub/be/mod01/category/", json={"user_id":"123","user_name":"guguldash","name": "Salary"})
            new_category = new_category_response.json()

            # Perform a credit transaction
            new_txn_response = client.post("/api/app24005_personal_hub/be/mod01/txn/", json={"user_id":"123","user_name":"guguldash","txn_title":"Salary Received", "txntype_name":"Credit", "txntype_id":"C", "from_acc_name":"", "from_acc_id":"", "to_acc_name":"ICICI", "to_acc_id":new_account["_id"], "amt":20000.00, "category_name":"Salary", "category_id":new_category["_id"], "txn_date": "2024-04-09"})
            new_txn = new_txn_response.json()
            
            # Reverse the credit transaction
            reverse_credit_txn_response = client.post("/api/app24005_personal_hub/be/mod01/txn/reverse/"+new_txn['ctxn']['_id'])
            assert reverse_credit_txn_response.status_code == 200
            reverse = reverse_credit_txn_response.json()
            reverse_bal=reverse['tacc']['balance']
            assert reverse_bal == new_account.get('balance')
            txn_type=reverse['ctxn']['txntype_name']
            assert txn_type == 'Reversed'


def test_reverse_txn_debit(capsys):
    with TestClient(app) as client:
        with capsys.disabled():

            # Create a new account
            new_account_response = client.post("/api/app24005_personal_hub/be/mod01/accoutn/", json={"user_id":"123","user_name":"guguldash","acc_title":"SBI", "acc_type_name": "Bank", "acc_type_id": "Bank", "balance": 5000.00})
            new_account = new_account_response.json()

            # Create a new category
            new_category_response = client.post("/api/app24005_personal_hub/be/mod01/category/", json={"user_id":"123","user_name":"guguldash","name":"Grocery"})
            new_category = new_category_response.json()

            # Perform a debit transaction
            new_txn_response = client.post("/api/app24005_personal_hub/be/mod01/txn/", json={"user_id":"123","user_name":"guguldash","txn_title":"Purchased Grocery", "txntype_name":"Debit", "txntype_id":"D", "from_acc_name":"SBI", "from_acc_id":new_account["_id"], "to_acc_name":"", "to_acc_id":"", "amt":300.00, "category_name":"Grocery", "category_id":new_category["_id"], "txn_date": "2024-05-09"})
            new_txn = new_txn_response.json()
            
            # Reverse the debit transaction
            reverse_credit_txn_response = client.post("/api/app24005_personal_hub/be/mod01/txn/reverse/"+new_txn['ctxn']['_id'])
            assert reverse_credit_txn_response.status_code == 200
            reverse = reverse_credit_txn_response.json()
            reverse_bal=reverse['facc']['balance']
            assert reverse_bal == new_account.get('balance')
            txn_type=reverse['ctxn']['txntype_name']
            assert txn_type == 'Reversed'
         
def test_reverse_txn_transfer(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            # Create a new account1
            new_account_response = client.post("/api/app24005_personal_hub/be/mod01/accoutn/", json={"user_id":"123","user_name":"guguldash","acc_title":"Piggy Bank", "acc_type_name": "Bank", "acc_type_id": "Bank", "balance": 2000.00})
            new_account1 = new_account_response.json()
            
            # Create a new account2
            new_account = client.post("/api/app24005_personal_hub/be/mod01/accoutn/", json={"user_id":"123","user_name":"guguldash","acc_title":"SBI", "acc_type_name": "Bank", "acc_type_id": "Bank", "balance": 5000.00})
            new_account2 = new_account.json()

            # Create a new category
            new_category_response = client.post("/api/app24005_personal_hub/be/mod01/category/", json={"user_id":"123","user_name":"guguldash","name":"Transfer"})
            new_category = new_category_response.json()

            # Perform a transfer transaction
            new_txn_response = client.post("/api/app24005_personal_hub/be/mod01/txn/", json={"user_id":"123","user_name":"guguldash","txn_title":"Money Transfered", "txntype_name":"Transfer", "txntype_id":"T", "from_acc_name":"Piggy Bank", "from_acc_id":new_account1["_id"], "to_acc_name":"SBI", "to_acc_id":new_account2["_id"], "amt":100.00, "category_name":"Transfer", "category_id":new_category["_id"], "txn_date": "2024-06-09"})
            new_txn = new_txn_response.json()
            
            # Reverse the transfer transaction
            reverse_credit_txn_response = client.post("/api/app24005_personal_hub/be/mod01/txn/reverse/"+new_txn['ctxn']['_id'])
            assert reverse_credit_txn_response.status_code == 200
            reverse = reverse_credit_txn_response.json()
            
            # Assert of from_account
            reverse_bal1=reverse['facc']['balance']
            assert reverse_bal1 == new_account1.get('balance')
            
            # Assert of to_account
            reverse_bal2=reverse['tacc']['balance']
            assert reverse_bal2 == new_account2.get('balance')
            
            # Assert of transaction type
            txn_type=reverse['ctxn']['txntype_name']
            assert txn_type == 'Reversed'
          

         
# TEST CASE FOR LIST        
def test_list_txn(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            # print('test_list_txn')
            new_account_response = client.post("/api/app24005_personal_hub/be/mod01/accoutn/", json={"user_id":"123","user_name":"guguldash","acc_title":"ICICI", "acc_type_name": "Bank", "acc_type_id": "Bank", "balance": 1000.00})
            new_account = new_account_response.json()
            new_category_response = client.post("/api/app24005_personal_hub/be/mod01/category/", json={"user_id":"123","user_name":"guguldash","name":"Salary"})
            new_category = new_category_response.json()
            new_txn_response = client.post("/api/app24005_personal_hub/be/mod01/txn/", json={"user_id":"123","user_name":"guguldash","txn_title":"Salary Received", "txntype_name":"Credit", "txntype_id":"Credit", "from_acc_name":"abc", "from_acc_id":"abc", "to_acc_name":"ICICI", "to_acc_id":new_account["_id"], "amt":20000.00, "category_name":"Salary", "category_id":new_category["_id"], "txn_date": "2024-04-09"})
            assert new_txn_response.status_code == 201
            get_transactions_response = client.get("/api/app24005_personal_hub/be/mod01/accoutn/")
            assert get_transactions_response.status_code == 200
            transactions = get_transactions_response.json()
            assert len(transactions) > 0        

#TEST CASE FIND      
def test_find_txn(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            # print('test_find_txn')
            new_account_response = client.post("/api/app24005_personal_hub/be/mod01/accoutn/", json={"user_id":"123","user_name":"guguldash","acc_title":"ICICI", "acc_type_name": "Bank", "acc_type_id": "Bank", "balance": 1000.00})
            new_account = new_account_response.json()
            
            new_category_response = client.post("/api/app24005_personal_hub/be/mod01/category/", json={"user_id":"123","user_name":"guguldash","name":"Salary"})
            new_category = new_category_response.json()
            
            new_txn = client.post("/api/app24005_personal_hub/be/mod01/txn/", json={"user_id":"123","user_name":"guguldash","txn_title":"Salary Received", "txntype_name":"Credit", "txntype_id":"Credit", "from_acc_name":"abc", "from_acc_id":"abc", "to_acc_name":"ICICI", "to_acc_id":new_account["_id"], "amt":20000.00, "category_name":"Salary", "category_id":new_category["_id"], "txn_date": "2024-04-09"}).json()
            get_txn_response = client.get("/api/app24005_personal_hub/be/mod01/txn/" + new_txn['ctxn']['_id'])
            assert get_txn_response.status_code == 200
            assert get_txn_response.json() == new_txn['ctxn']
          
                
#testcase for negative            
def test_get_txn_unexisting(capsys):
   with TestClient(app) as client:
        with capsys.disabled():
            get_txn_response = client.get("/api/app24005_personal_hub/be/mod01/txn/unexisting_id")
            assert get_txn_response.status_code == 404


