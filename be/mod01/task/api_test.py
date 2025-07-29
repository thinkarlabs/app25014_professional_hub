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
def test_create_task(capsys):
    with TestClient(app) as client:
        with capsys.disabled(): 
            print('Testing task create')
            new_project = client.post("/api/app24005_personal_hub/be/mod01/project/", json={"user_id":"123","user_name":"guguldash","project_title": "Money Management"}).json()
            new_task = client.post("/api/app24005_personal_hub/be/mod01/task/",json={"user_id":"123","user_name":"guguldash","type_id":new_project.get("_id"),"title":"Write Sample Test","owner_name":"Srivastava","owner_id":"o","reminder_date":"2030-03-24","project_id":"TM","project_name":"Task Managment","status_id":"CP","status_name":"Completed","desc":"comp"})
            assert new_task.status_code == 201
            body = new_task.json()
            assert body.get("title") == "Write Sample Test"
            assert body.get("owner_name") == "Srivastava"
            assert body.get("owner_id") == "o"
            assert body.get("reminder_date") == "2030-03-24"
            assert body.get("project_id") == "TM"
            assert body.get("project_name") == "Task Managment"
            assert body.get("status_id") == "CP"
            assert body.get("status_name") == "Completed"
            assert body.get("desc") == "comp"
            assert body.get("user_id") == "123"
            assert body.get("user_name") == "guguldash"
            assert "_id" in body
                  
            
            
 
#TEST CASE FOR LIST#        
def test_list_task(capsys):
 
    with TestClient(app) as client:
      with capsys.disabled():
            print('test_list_task')      
            app.database["tasks"].drop()

            new_project = client.post("/api/app24005_personal_hub/be/mod01/project/", json={"user_id":"123","user_name":"guguldash","title": "Money Management"}).json()
            new_task = client.post("/api/app24005_personal_hub/be/mod01/task/",json={"user_id":"123","user_name":"guguldash","type_id":new_project.get("_id"),"title":"Write Sample Test","owner_name":"Srivastava","owner_id":"o","reminder_date":"2030-03-24","project_id":"TM","project_name":"Task Managment","status_id":"CP","status_name":"Completed","desc":"comp"})
            get_tasks_response = client.get("/api/app24005_personal_hub/be/mod01/task/")
            print("c..........",get_tasks_response.json())
            assert get_tasks_response.status_code == 200
     

 
#TEST CASE DELETE#           
def test_delete_task(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_delete_task')
            new_project = client.post("/api/app24005_personal_hub/be/mod01/project/", json={"user_id":"123","user_name":"guguldash","title": "Money Management"}).json()
            new_task = client.post("/api/app24005_personal_hub/be/mod01/task/",json={"user_id":"123","user_name":"guguldash","type_id":new_project.get("_id"),"title":"Write Sample Test","owner_name":"Srivastava","owner_id":"o","reminder_date":"2030-03-24","project_id":"TM","project_name":"Task Managment","status_id":"CP","status_name":"Completed","desc":"comp"}).json()
            delete_task_response = client.delete("/api/app24005_personal_hub/be/mod01/task/" + new_task.get("_id"))
            assert delete_task_response.status_code == 204 


#TEST CASE FIND#       
def test_get_task(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_get_find')
            new_task_response = client.post("/api/app24005_personal_hub/be/mod01/task/", json={"user_id":"123","user_name":"guguldash","title": "Write Sample Test","owner_name":"Srivastava","owner_id":"o","reminder_date": "2030-03-24", "project_id": "TM", "project_name": "Task Management", "status_id": "CP", "status_name": "Completed", "desc": "comp"}).json()
            get_task_response = client.get("/api/app24005_personal_hub/be/mod01/task/" + new_task_response.get("_id"))
            assert get_task_response.status_code == 200
            assert get_task_response.json() == new_task_response
   
  
#TEST CASE FOR UPDATES#   
def test_update_title(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_title')
            new_task_response = client.post("/api/app24005_personal_hub/be/mod01/task/", json={"user_id":"123","user_name":"guguldash","title": "Write Sample Test","owner_name":"Srivastava","owner_id":"o","reminder_date": "2030-03-24", "project_id": "TM", "project_name": "Task Management", "status_id": "CP", "status_name": "Completed", "desc": "comp"}).json()
            response = client.post("/api/app24005_personal_hub/be/mod01/task/" + new_task_response.get("_id"), json={"title":"Write Sample Test-Updated"})
            assert response.status_code == 200
            assert response.json().get("title") == "Write Sample Test-Updated"
 
#TEST CASE FOR OWNER UPDATE#    
def test_update_owner_name(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_owner_name')
            new_task_response = client.post("/api/app24005_personal_hub/be/mod01/task/", json={"user_id":"123","user_name":"guguldash","title": "Write Sample Test","owner_name":"Srivastava","owner_id":"o","reminder_date": "2030-03-24", "project_id": "TM", "project_name": "Task Management", "status_id": "CP", "status_name": "Completed", "desc": "comp"}).json()
            response = client.post("/api/app24005_personal_hub/be/mod01/task/" +new_task_response.get("_id"), json={"owner_name": "Srivastava-Updated"})
            assert response.status_code == 200
            assert response.json().get("owner_name") == "Srivastava-Updated"

#TEST CASE FOR REMINDER UPDATE#                  
def test_update_reminder_date(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_reminder_date')
            new_task_response = client.post("/api/app24005_personal_hub/be/mod01/task/", json={"user_id":"123","user_name":"guguldash","title": "Write Sample Test","owner_name":"Srivastava","owner_id":"o","reminder_date": "2030-03-24", "project_id": "TM", "project_name": "Task Management", "status_id": "CP", "status_name": "Completed", "desc": "comp"}).json()
            response = client.post("/api/app24005_personal_hub/be/mod01/task/" + new_task_response.get("_id"), json={"reminder_date": "2023-01-13"})
            assert response.status_code == 200
            assert response.json().get("reminder_date") == "2023-01-13"
    
            
            
#TEST CASE FOR PROJECT NAME UPDATE#                
def test_update_project_name(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_project_name')
            new_task_response = client.post("/api/app24005_personal_hub/be/mod01/task/", json={"user_id":"123","user_name":"guguldash","title": "Write Sample Test","owner_name":"Srivastava","owner_id":"o","reminder_date": "2030-03-24", "project_id": "TM", "project_name": "Task Management", "status_id": "CP", "status_name": "Completed", "desc": "comp"}).json()
            response = client.post("/api/app24005_personal_hub/be/mod01/task/" + new_task_response.get("_id"), json={"project_name" : "Task Managment-Updated"})
            assert response.status_code == 200 
            assert response.json().get("project_name") == "Task Managment-Updated"
    
            
#TEST CASE FOR DESC UPDATE#    
def test_update_desc(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_dec')
            new_task_response = client.post("/api/app24005_personal_hub/be/mod01/task/", json={"user_id":"123","user_name":"guguldash","title": "Write Sample Test","owner_name":"Srivastava","owner_id":"o","reminder_date": "2030-03-24", "project_id": "TM", "project_name": "Task Management", "status_id": "CP", "status_name": "Completed", "desc": "comp"}).json()
            response = client.post("/api/app24005_personal_hub/be/mod01/task/" + new_task_response.get("_id"), json={"desc" : "comp-Updated"})
            assert response.status_code == 200
            assert response.json().get("desc") == "comp-Updated"            

            
           
# NEGATIVE DETAILS        
def test_create_task_missing_title(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_create_task_missing_title')
            get_task_response = client.post("/api/app24005_personal_hub/be/mod01/task/",json={"title":"Write Sample Test","owner_name":"Srivastava","owner_id":"o","reminder_date":"2030-03-24","project_id":"TM","project_name":"Task Managment","status_id":"CP","status_name":"Completed","desc":"comp"}).json()
            get_task_response = client.get("/api/app24005_personal_hub/be/mod01/task/unexisting_id")
            assert get_task_response.status_code == 404


# NEGATIVE TEST CASE MISSING TASK WONER#                 
def test_create__missing_task_owner(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_create__missing_task_owner')
            get_task_response = client.post("/api/app24005_personal_hub/be/mod01/task/",json={"title":"Write Sample Test","owner_name":"Srivastava","owner_id":"o","reminder_date":"2030-03-24","project_id":"TM","project_name":"Task Managment","status_id":"CP","status_name":"Completed","desc":"comp"}).json()
            get_task_response = client.get("/api/app24005_personal_hub/be/mod01/task/unexisting_id")
            assert get_task_response.status_code == 404

# NEGATIVE TEST CASE MISSING REMINDER DAT#                 
def test_create_task_missing_reminder_date(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_create_task_missing_reminder_date')
            get_task_response = client.post("/api/app24005_personal_hub/be/mod01/task/",json={"title":"Write Sample Test","owner_name":"Srivastava","owner_id":"o","reminder_date":"2030-03-24","project_id":"TM","project_name":"Task Managment","status_id":"CP","status_name":"Completed","desc":"comp"}).json()
            get_task_response = client.get("/api/app24005_personal_hub/be/mod01/task/unexisting_id")
            assert get_task_response.status_code == 404
            
# NEGATIVE TEST CASE MISSING PROJECT NAME#                        
def test_create_task_missing_project_name(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_create_donor_missing_project_name')
            get_task_response = client.post("/api/app24005_personal_hub/be/mod01/task/",json={"title":"Write Sample Test","owner_name":"Srivastava","owner_id":"o","reminder_date":"2030-03-24","project_id":"TM","project_name":"Task Managment","status_id":"CP","status_name":"Completed","desc":"comp"}).json()
            get_task_response = client.get("/api/app24005_personal_hub/be/mod01/task/unexisting_id")
            assert get_task_response.status_code == 404

# NEGATIVE TEST CASE MISSING STATUS NAME#                                   
def test_create_task_missing_status_name(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_create_task_missing_status_name')
            get_task_response = client.post("/api/app24005_personal_hub/be/mod01/task/",json={"user_id":"123","user_name":"guguldash","title":"Write Sample Test","owner_name":"Srivastava","owner_id":"o","reminder_date":"2030-03-24","project_id":"TM","project_name":"Task Managment","status_id":"CP","status_name":"Completed","desc":"comp"}).json()
            get_task_response = client.get("/api/app24005_personal_hub/be/mod01/task/unexisting_id")
            assert get_task_response.status_code == 404           

# NEGATIVE TEST CASE MISSING DESC#                        
def test_create_task_missing_desc(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_create_donor_missing_contact_phone')
            response = client.post("/api/app24005_personal_hub/be/mod01/task/",json={"user_id":"123","user_name":"guguldash","title":"Write Sample Test","owner_name":"Srivastava","owner_id":"o","reminder_date":"2030-03-24","project_id":"TM","project_name":"Task Managment","status_id":"CP","desc":"comp","status_name":"Completed"}).json()
            get_task_response = client.get("/api/app24005_personal_hub/be/mod01/task/unexisting_id")
            assert get_task_response.status_code == 404

 
# NEGATIVE TEST CASE FOR DELETE#                        
def test_delete_task_unexisting(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_delete_task_unexisting')
            delete_task_response = client.delete("/api/app24005_personal_hub/be/mod01/task/unexisting_id")
            assert delete_task_response.status_code == 404
            
# NEGATIVE TEST CASE FOR UNEXISTING#                                
def test_get_task_unexisting(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_get_task_unexisting')
            get_task_response = client.get("/api/app24005_personal_hub/be/mod01/task/sunexisting_id")
            assert get_task_response.status_code == 404
            
