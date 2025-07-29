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

#TEST CASE FOR CREATE#
def test_create_assettype(capsys):
    with TestClient(app) as client:
        with capsys.disabled(): 
            response = client.post("/api/app24005_personal_hub/be/mod01/assettype/",json={"user_id":"123","user_name":"guguldash","title": "laptop"})
            assert response.status_code == 201
            body = response.json()
            assert body.get("title") == "laptop"      
            assert body.get("user_id") == "123"      
            assert body.get("user_name") == "guguldash"      
            assert "_id" in body
            
         
#TEST CASE FOR LIST#        
def test_list_assettype(capsys): 
    with TestClient(app) as client:
      with capsys.disabled(): 
        get_assettypes_response = client.get("/api/app24005_personal_hub/be/mod01/assettype/")
        assert get_assettypes_response.status_code == 200
     
#TEST CASE FOR DELETE#       
def test_delete_assettype(capsys):
    with TestClient(app) as client:
      with capsys.disabled():
        print('test_delete_assettype...')
        new_assettype = client.post("/api/app24005_personal_hub/be/mod01/assettype/",json={"user_id":"123","user_name":"guguldash","title": "laptop"}).json()
        delete_assettype_response = client.delete("/api/app24005_personal_hub/be/mod01/assettype/" + new_assettype.get("_id"))
        assert delete_assettype_response.status_code == 204
 
#TEST CASE FIND#       
def test_get_assettype(capsys):
    with TestClient(app) as client:
       with capsys.disabled():  
        print('test_find_assettype...')
        new_assettype = client.post("/api/app24005_personal_hub/be/mod01/assettype/",json={"user_id":"123","user_name":"guguldash","title": "laptop"}).json() 

        get_assettype_response = client.get("/api/app24005_personal_hub/be/mod01/assettype/" + new_assettype.get("_id"))
        assert get_assettype_response.status_code == 200
        assert get_assettype_response.json() == new_assettype
        
#TEST CASE FOR UPDATE#       
def test_update_assettype_title(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print("test_update_assettype_title...")
            new_assettype = client.post("/api/app24005_personal_hub/be/mod01/assettype/",json={"user_id":"123","user_name":"guguldash","title": "laptop"}).json()
            print(new_assettype.get("_id"))
            response = client.post("/api/app24005_personal_hub/be/mod01/assettype/" + str(new_assettype.get("_id")), json={"title": "laptop-Updated"})
           
            assert response.status_code == 200
            assert response.json().get("title") == "laptop-Updated"            


#testcase for negative
 
def test_delete_assettype_unexisting(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            delete_asset_response = client.delete("/api/app24005_personal_hub/be/mod01/assettype/unexisting_id")
            assert delete_asset_response.status_code == 404 

def test_get_assettype_unexisting(capsys):
   with TestClient(app) as client:
        with capsys.disabled():
            get_asset_response = client.get("/api/app24005_personal_hub/be/mod01/assettype/unexisting_id")
            assert get_asset_response.status_code == 404
