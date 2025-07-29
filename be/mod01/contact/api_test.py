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
def test_create_contact(capsys):
    with TestClient(app) as client:
        with capsys.disabled(): 
            response = client.post("/api/app24005_personal_hub/be/mod01/contact/",json={"user_id":"123","user_name":"guguldash","contact_name": "neha","phone_no": "9871956877","email":"neha@gmail.com","gender_id":"F","gender_name":"Female"})
            assert response.status_code == 201
            body = response.json()
            assert body.get("contact_name") == "neha" 
            assert body.get("phone_no") == "9871956877"      
            assert body.get("email") == "neha@gmail.com"      
            assert body.get("gender_id") == "F"  
            assert body.get("gender_name") == "Female"  
            assert body.get("user_id") == "123"  
            assert body.get("user_name") == "guguldash"  
            assert "_id" in body
           
#TEST CASE FOR LIST#        
def test_list_contact(capsys): 
    with TestClient(app) as client:
      with capsys.disabled(): 
        get_contact_response = client.get("/api/app24005_personal_hub/be/mod01/contact/")
        assert get_contact_response.status_code == 200
     
#TEST CASE FOR DELETE#       
def test_delete_contact(capsys):
    with TestClient(app) as client:
      with capsys.disabled():
        print('test_delete_contact...')
        new_contact = client.post("/api/app24005_personal_hub/be/mod01/contact/",json={"user_id":"123","user_name":"guguldash","contact_name": "neha","phone_no": "9871956877","email":"neha@gmail.com","gender_id":"F","gender_name":"Female"}).json()
        delete_contact_response = client.delete("/api/app24005_personal_hub/be/mod01/contact/" + new_contact.get("_id"))
        assert delete_contact_response.status_code == 204
 
#TEST CASE FIND#       
def test_get_contact(capsys):
    with TestClient(app) as client:
       with capsys.disabled():  
        print('test_find_contact...')
        new_contact = client.post("/api/app24005_personal_hub/be/mod01/contact/",json={"user_id":"123","user_name":"guguldash","contact_name": "neha","phone_no": "9871956877","email":"neha@gmail.com","gender_id":"F","gender_name":"Female"}).json()

        get_contact_response = client.get("/api/app24005_personal_hub/be/mod01/contact/" + new_contact.get("_id"))
        assert get_contact_response.status_code == 200
        assert get_contact_response.json() == new_contact
        
#TEST CASE FOR UPDATE#       
def test_update_contact_name(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print("test_update_contact_name...")
            new_contact = client.post("/api/app24005_personal_hub/be/mod01/contact/",json={"user_id":"123","user_name":"guguldash","contact_name": "neha","phone_no": "9871956877","email":"neha@gmail.com","gender_id":"F","gender_name":"Female"}).json()
            print(new_contact.get("_id"))
            response = client.post("/api/app24005_personal_hub/be/mod01/contact/" + str(new_contact.get("_id")), json={"contact_name": "naveen"})
           
            assert response.status_code == 200
            assert response.json().get("contact_name") == "naveen"            


#testcase for negative
 
def test_delete_contact_unexisting(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            delete_contact_response = client.delete("/api/app24005_personal_hub/be/mod01/contact/unexisting_id")
            assert delete_contact_response.status_code == 404 

def test_get_contact_unexisting(capsys):
   with TestClient(app) as client:
        with capsys.disabled():
            get_contact_response = client.get("/api/app24005_personal_hub/be/mod01/contact/unexisting_id")
            assert get_contact_response.status_code == 404

