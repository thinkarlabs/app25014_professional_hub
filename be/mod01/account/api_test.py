import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from dotenv import dotenv_values
from pymongo import MongoClient
from space.app00_neev.be.main.app import app as base_app
from store.app25014_professional_hub.be.main.app import app


config = dotenv_values(".env")
app.database = app.mongodb_client[app.dbname + "_test"]
base_app.database = base_app.mongodb_client[base_app.dbname + "_test"]



#TEST CASE FOR CREATE
def test_create_account(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_create_account')
            response = client.post("/api/app25014_professional_hub/be/mod01/accoutn/", json={"user_id":"123","user_name":"guguldash","acc_title":"ICICI", "acc_type_name": "Bank", "acc_type_id": "Bank", "balance": 1000.00})
            assert response.status_code == 201
            body = response.json()
            assert body.get("acc_title") == "ICICI"
            assert body.get("acc_type_name") == "Bank"
            assert body.get("acc_type_id") == "Bank"
            assert body.get("balance") == 1000.00
            assert body.get("user_id") == "123"
            assert body.get("user_name") == "guguldash"
            assert "_id" in body

#TEST CASE FOR LIST        
def test_list_account(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_list_account')
            get_accounts_response = client.get("/api/app25014_professional_hub/be/mod01/accoutn/")
            assert get_accounts_response.status_code == 200
       
#TEST CASE FOR DELETE       
def test_delete_account(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_delete_account')
            new_account = client.post("/api/app25014_professional_hub/be/mod01/accoutn/", json={"user_id":"123","user_name":"guguldash","acc_title":"ICICI", "acc_type_name": "Bank", "acc_type_id": "Bank", "balance": 1000.00}).json()
            delete_account_response = client.delete("/api/app25014_professional_hub/be/mod01/accoutn/" + new_account.get("_id"))
            assert delete_account_response.status_code == 204

#TEST CASE FIND      
def test_find_account(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_find_account')
            new_account =client.post("/api/app25014_professional_hub/be/mod01/accoutn/", json={"user_id":"123","user_name":"guguldash","acc_title":"ICICI", "acc_type_name": "Bank", "acc_type_id": "Bank", "balance": 1000.00}).json()
            get_accounts_response = client.get("/api/app25014_professional_hub/be/mod01/accoutn/" + new_account.get("_id"))
            assert get_accounts_response.status_code == 200
            assert get_accounts_response.json() == new_account
#TEST CASE FOR UPDATE       
def test_update_acc_title(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print("test_update_acc_title")
            new_account =client.post("/api/app25014_professional_hub/be/mod01/accoutn/", json={"user_id":"123","user_name":"guguldash","acc_title":"ICICI", "acc_type_name": "Bank", "acc_type_id": "Bank", "balance": 1000.00}).json()
            response = client.post("/api/app25014_professional_hub/be/mod01/accoutn/" + new_account.get("_id"), json={"acc_title": "SBI"})
            assert response.status_code == 200
            assert response.json().get("acc_title") == "SBI"
        

      
def test_update_acc_type(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print("test_update_acc_type")
            new_account =client.post("/api/app25014_professional_hub/be/mod01/accoutn/", json={"user_id":"123","user_name":"guguldash","acc_title":"ICICI", "acc_type_name": "Bank", "acc_type_id": "Bank", "balance": 1000.00}).json()
            response = client.post("/api/app25014_professional_hub/be/mod01/accoutn/" + new_account.get("_id"), json={"acc_type_name": "Cash"})
            assert response.status_code == 200
            assert response.json().get("acc_type_name") == "Cash"

def test_update_balance(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print("test_update_balance")
            new_account =client.post("/api/app24005_personal_hub/be/mod01/accoutn/", json={"user_id":"123","user_name":"guguldash","acc_title":"ICICI", "acc_type_name": "Bank", "acc_type_id": "Bank", "balance": 1000.00}).json()
            response = client.post("/api/app24005_personal_hub/be/mod01/accoutn/" + new_account.get("_id"), json={"balance": 8000.00})
            assert response.status_code == 200
            assert response.json().get("balance") == 8000.00




# NEGATIVE TESTCASE
def test_delete_account_unexisting(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_delete_account_unexisting...')
            delete_account_response = client.delete("/api/app25014_professional_hub/be/mod01/accoutn/unexisting_id")
            assert delete_account_response.status_code == 404 

def test_get_account_unexisting(capsys):
   with TestClient(app) as client:
        with capsys.disabled():
            print("test_get_account_unexisting...")
            get_account_response = client.get("/api/app25014_professional_hub/be/mod01/accoutn/accoutn/unexisting_id")
            assert get_account_response.status_code == 404

