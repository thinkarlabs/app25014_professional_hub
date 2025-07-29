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
def test_create_project(capsys):
    with TestClient(app) as client:
        with capsys.disabled(): 
            print('test_create_project...')
            response = client.post("/api/app24005_personal_hub/be/mod01/project/",json={"user_id":"123","user_name":"guguldash","project_title":"Task Managment","status_name":"Active","status_id":"A"})
            assert response.status_code == 201
            body = response.json()
            assert body.get("project_title") == "Task Managment"
            assert body.get("status_name") == "Active"
            assert body.get("status_id") == "A"
            assert body.get("user_id") == "123"
            assert body.get("user_name") == "guguldash"

            assert "_id" in body


#TEST CASE FOR LIST#        
def test_list_project(capsys): 
    with TestClient(app) as client:
      with capsys.disabled(): 
        print('test_list_project...')
        get_project_response = client.get("/api/app24005_personal_hub/be/mod01/project/")
        assert get_project_response.status_code == 200
 

#TEST CASE FOR DELEE#    
def test_delete_project(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
          print('test_delete_project...')
        new_project = client.post("/api/app24005_personal_hub/be/mod01/project/", json={"user_id":"123","user_name":"guguldash","project_title":"Task Managment","status_name":"Active","status_id":"A"}).json()

        delete_project_response = client.delete("/api/app24005_personal_hub/be/mod01/project/" + new_project.get("_id"))
        assert delete_project_response.status_code == 204
     
        
#TEST CASE FOR FIND#
def test_get_project(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
           print('test_get_project...')
        new_project = client.post("/api/app24005_personal_hub/be/mod01/project/", json={"user_id":"123","user_name":"guguldash","project_title":"Task Managment","status_name":"Active","status_id":"A"}).json()

        get_project_response = client.get("/api/app24005_personal_hub/be/mod01/project/" + new_project.get("_id"))
        assert get_project_response.status_code == 200
        assert get_project_response.json() == new_project


#TEST CASE FOR TITLE# 
def test_update_project_title(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print("test_update_project_title...")
            new_project = client.post("/api/app24005_personal_hub/be/mod01/project/", json={"user_id":"123","user_name":"guguldash","project_title":"Task Managment","status_name":"Active","status_id":"A"}).json()
            print(new_project.get("_id"))
            response = client.post("/api/app24005_personal_hub/be/mod01/project/" + str(new_project.get("_id")), json={"project_title": "Task Managment-Updated"})
            assert response.status_code == 200
            assert response.json().get("project_title") == "Task Managment-Updated" 


#TEST CASE FOR STATUS NAME# 
def test_update_status_name(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print("test_status_name...")
            new_project = client.post("/api/app24005_personal_hub/be/mod01/project/", json={"user_id":"123","user_name":"guguldash","project_title":"Task Managment","status_name":"Active","status_id":"A"}).json()
            print(new_project.get("_id"))
            response = client.post("/api/app24005_personal_hub/be/mod01/project/" + str(new_project.get("_id")), json={"status_name": "inactive-Updated"})
            assert response.status_code == 200
            assert response.json().get("status_name") == "inactive-Updated" 


#TEST CASE FOR STATUS_id# 
def test_update_status_id(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print("test_update_status_id...")
            new_project = client.post("/api/app24005_personal_hub/be/mod01/project/", json={"user_id":"123","user_name":"guguldash","project_title":"Task Managment","status_name":"Active","status_id":"A"}).json()
            print(new_project.get("_id"))
            response = client.post("/api/app24005_personal_hub/be/mod01/project/" + str(new_project.get("_id")), json={"status_id": "A-Updated"})
            assert response.status_code == 200
            assert response.json().get("status_id") == "A-Updated" 


#TEST CASE FOR negative#
def test_delete_project_unexisting(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_delete_project_unexisting...')
            delete_project_response = client.delete("/api/app24005_personal_hub/be/mod01/project/unexisting_id")
            assert delete_project_response.status_code == 404 


#TEST CASE FOR negative#
def test_get_project_unexisting(capsys):
   with TestClient(app) as client:
        with capsys.disabled():
            print("test_get_project_unexisting...")
            get_project_response = client.get("/api/app24005_personal_hub/be/mod01/project/unexisting_id")
            assert get_project_response.status_code == 404
