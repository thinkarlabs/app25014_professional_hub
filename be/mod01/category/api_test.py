import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from dotenv import dotenv_values
from pymongo import MongoClient
from space.app00_neev.be.main.app import app as base_app
from store.app24005_personal_hub.be.main.app import app


config = dotenv_values(".env")
app.database = app.mongodb_client[app.dbname + "_test"]
base_app.database = base_app.mongodb_client[base_app.dbname + "_test"]


#TEST CASE FOR CREATE
def test_create_category(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_create_category')
            response = client.post("/api/app24005_personal_hub/be/mod01/category/", json={"user_id":"123","user_name":"guguldash","name":"Salary"})
            assert response.status_code == 201
            body = response.json()
            assert body.get("name") == "Salary"
            assert body.get("user_id") == "123"
            assert body.get("user_name") == "guguldash"
            assert "_id" in body

#TEST CASE FOR LIST        
def test_list_category(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_list_category')
            get_categories_response = client.get("/api/app24005_personal_hub/be/mod01/category/")
            assert get_categories_response.status_code == 200
       
#TEST CASE FOR DELETE       
def test_delete_category(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_delete_category')
            new_category = client.post("/api/app24005_personal_hub/be/mod01/category/", json={"user_id":"123","user_name":"guguldash","name":"Salary"}).json()
            delete_account_response = client.delete("/api/app24005_personal_hub/be/mod01/category/" + new_category.get("_id"))
            assert delete_account_response.status_code == 204

#TEST CASE FIND      
def test_find_category(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_find_category')
            new_category = client.post("/api/app24005_personal_hub/be/mod01/category/", json={"user_id":"123","user_name":"guguldash","name":"Salary"}).json()
            get_accounts_response = client.get("/api/app24005_personal_hub/be/mod01/category/" + new_category.get("_id"))
            assert get_accounts_response.status_code == 200
            assert get_accounts_response.json() == new_category
            
            

#TEST CASE FOR UPDATE       
def test_update_name(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print("test_update_name")
            new_category = client.post("/api/app24005_personal_hub/be/mod01/category/", json={"user_id":"123","user_name":"guguldash","name": "Salary"}).json()
            response = client.post("/api/app24005_personal_hub/be/mod01/category/" + new_category.get("_id"), json={"name": "Rent"})
            assert response.status_code == 200
            assert response.json().get("name") == "Rent"




# NAGTIVE TESTCASEQ
def test_delete_category_unexisting(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_delete_category_unexisting...')
            delete_category_response = client.delete("/api/app24005_personal_hub/be/mod01/category/unexisting_id")
            assert delete_category_response.status_code == 404 

def test_get_category_unexisting(capsys):
   with TestClient(app) as client:
        with capsys.disabled():
            print("test_get_txn_unexisting...")
            get_category_response = client.get("/api/app24005_personal_hub/be/mod01/category/unexisting_id")
            assert get_category_response.status_code == 404

