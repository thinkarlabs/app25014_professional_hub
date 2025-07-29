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
def test_create_asset(capsys):
    with TestClient(app) as client:
        with capsys.disabled(): 
            new_assettype = client.post("/api/app24005_personal_hub/be/mod01/assettype/", json={"user_id":"123","user_name":"guguldash","title": "laptop"}).json()
            new_contact = client.post("/api/app24005_personal_hub/be/mod01/contact/",json={"user_id":"123","user_name":"guguldash","contact_name": "neha","phone_no": "9871956877","email":"neha@gmail.com","gender_id":"F","gender_name":"Female"}).json()
            new_asset = client.post("/api/app24005_personal_hub/be/mod01/asset/",json={"user_id":"123","user_name":"guguldash","type_id":new_assettype.get("_id"),"type_name": "Laptop","title":"Dell","desc":"Laptop is dell company","purch_date": "2020-03-20","contact_id":new_contact.get("_id"),"contact_name":'Neha',"price":20000,"warantydetail":"From a company or a person to repair or replace a product(1year)","identifier":"VGN-FW550F"})
            assert new_asset.status_code == 201
            
            
#TEST CASE FOR LIST#        
def test_list_asset(capsys):
    expected_asset_count = 1
    with TestClient(app) as client:
      with capsys.disabled():  
            app.database["assets"].drop()
            print("asset count:")
 
            new_assettype = client.post("/api/app24005_personal_hub/be/mod01/assettype/", json={"user_id":"123","user_name":"guguldash","title": "laptop"}).json()
            new_contact = client.post("/api/app24005_personal_hub/be/mod01/contact/",json={"user_id":"123","user_name":"guguldash","contact_name": "neha","phone_no": "9871956877","email":"neha@gmail.com","gender_id":"F","gender_name":"Female"}).json()
            new_asset = client.post("/api/app24005_personal_hub/be/mod01/asset/",json={"user_id":"123","user_name":"guguldash","type_id":new_assettype.get("_id"),"type_name": "Laptop","title":"Dell","desc":"Laptop is dell company","purch_date": "2020-03-20","contact_id":new_contact.get("_id"),"contact_name":'Neha',"price":20000,"warantydetail":"From a company or a person to repair or replace a product(1year)","identifier":"VGN-FW550F"})


            get_assets_response = client.get("/api/app24005_personal_hub/be/mod01/asset/")
            asset = get_assets_response.json()
            assert get_assets_response.status_code == 200
            asset_count = len(asset)
            print("assets:",asset_count)
            assert asset_count == expected_asset_count

#TEST CASE FOR DELETE#       
def test_delete_asset(capsys):
    with TestClient(app) as client:
      with capsys.disabled():
            new_assettype = client.post("/api/app24005_personal_hub/be/mod01/assettype/", json={"user_id":"123","user_name":"guguldash","title": "laptop"}).json()
            new_contact = client.post("/api/app24005_personal_hub/be/mod01/contact/",json={"user_id":"123","user_name":"guguldash","contact_name": "neha","phone_no": "9871956877","email":"neha@gmail.com","gender_id":"F","gender_name":"Female"}).json()
            new_asset = client.post("/api/app24005_personal_hub/be/mod01/asset/",json={"user_id":"123","user_name":"guguldash","type_id":new_assettype.get("_id"),"type_name": "Laptop","title":"Dell","desc":"Laptop is dell company","purch_date": "2020-03-20","contact_id":new_contact.get("_id"),"contact_name":'Neha',"price":20000,"warantydetail":"From a company or a person to repair or replace a product(1year)","identifier":"VGN-FW550F"}).json()

            delete_asset_response = client.delete("/api/app24005_personal_hub/be/mod01/asset/" + new_asset.get("_id"))
            assert delete_asset_response.status_code == 204
            

#TEST CASE FIND#       
def test_get_asset(capsys):
    with TestClient(app) as client:
       with capsys.disabled():  
            new_assettype = client.post("/api/app24005_personal_hub/be/mod01/assettype/", json={"user_id":"123","user_name":"guguldash","title": "laptop"}).json()
            new_contact = client.post("/api/app24005_personal_hub/be/mod01/contact/",json={"user_id":"123","user_name":"guguldash","contact_name": "neha","phone_no": "9871956877","email":"neha@gmail.com","gender_id":"F","gender_name":"Female"}).json()
            new_asset = client.post("/api/app24005_personal_hub/be/mod01/asset/",json={"user_id":"123","user_name":"guguldash","type_id":new_assettype.get("_id"),"type_name": "Laptop","title":"Dell","desc":"Laptop is dell company","purch_date": "2020-03-20","contact_id":new_contact.get("_id"),"contact_name":'Neha',"price":20000,"warantydetail":"From a company or a person to repair or replace a product(1year)","identifier":"VGN-FW550F"}).json()

            get_asset_response = client.get("/api/app24005_personal_hub/be/mod01/asset/" + new_asset.get("_id"))
            assert get_asset_response.status_code == 200
            assert get_asset_response.json() == new_asset
            
#TEST CASE FOR UPDATE#       
def test_update_type_id(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            new_assettype = client.post("/api/app24005_personal_hub/be/mod01/assettype/", json={"user_id":"123","user_name":"guguldash","title": "laptop"}).json()
            new_contact = client.post("/api/app24005_personal_hub/be/mod01/contact/",json={"user_id":"123","user_name":"guguldash","contact_name": "neha","phone_no": "9871956877","email":"neha@gmail.com","gender_id":"F","gender_name":"Female"}).json()
            new_asset = client.post("/api/app24005_personal_hub/be/mod01/asset/",json={"user_id":"123","user_name":"guguldash","type_id":new_assettype.get("_id"),"type_name": "Laptop","title":"Dell","desc":"Laptop is dell company","purch_date": "2020-03-20","contact_id":new_contact.get("_id"),"contact_name":'Neha',"price":20000,"warantydetail":"From a company or a person to repair or replace a product(1year)","identifier":"VGN-FW550F"}).json()
            response = client.post("/api/app24005_personal_hub/be/mod01/asset/" + str(new_asset.get("_id")), json={"type_id": "6-Updated"})
           
            assert response.status_code == 200
            assert response.json().get("type_id") == "6-Updated"          
            

def test_update_type_name(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            new_assettype = client.post("/api/app24005_personal_hub/be/mod01/assettype/", json={"user_id":"123","user_name":"guguldash","title": "laptop"}).json()
            new_contact = client.post("/api/app24005_personal_hub/be/mod01/contact/",json={"user_id":"123","user_name":"guguldash","contact_name": "neha","phone_no": "9871956877","email":"neha@gmail.com","gender_id":"F","gender_name":"Female"}).json()
            new_asset = client.post("/api/app24005_personal_hub/be/mod01/asset/",json={"user_id":"123","user_name":"guguldash","type_id":new_assettype.get("_id"),"type_name": "Laptop","title":"Dell","desc":"Laptop is dell company","purch_date": "2020-03-20","contact_id":new_contact.get("_id"),"contact_name":'Neha',"price":20000,"warantydetail":"From a company or a person to repair or replace a product(1year)","identifier":"VGN-FW550F"}).json()

            response = client.post("/api/app24005_personal_hub/be/mod01/asset/" + str(new_asset.get("_id")), json={"type_name": "Laptop smart"})
           
            assert response.status_code == 200
            assert response.json().get("type_name") == "Laptop smart"          
            
def test_update_title(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            new_assettype = client.post("/api/app24005_personal_hub/be/mod01/assettype/", json={"user_id":"123","user_name":"guguldash","title": "laptop"}).json()
            new_contact = client.post("/api/app24005_personal_hub/be/mod01/contact/",json={"user_id":"123","user_name":"guguldash","contact_name": "neha","phone_no": "9871956877","email":"neha@gmail.com","gender_id":"F","gender_name":"Female"}).json()
            new_asset = client.post("/api/app24005_personal_hub/be/mod01/asset/",json={"user_id":"123","user_name":"guguldash","type_id":new_assettype.get("_id"),"type_name": "Laptop","title":"Dell","desc":"Laptop is dell company","purch_date": "2020-03-20","contact_id":new_contact.get("_id"),"contact_name":'Neha',"price":20000,"warantydetail":"From a company or a person to repair or replace a product(1year)","identifier":"VGN-FW550F"}).json()
            response = client.post("/api/app24005_personal_hub/be/mod01/asset/" + str(new_asset.get("_id")), json={"title": "Hp"})
           
            assert response.status_code == 200
            assert response.json().get("title") == "Hp"          
            

def test_update_desc(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            new_assettype = client.post("/api/app24005_personal_hub/be/mod01/assettype/", json={"user_id":"123","user_name":"guguldash","title": "laptop"}).json()
            new_contact = client.post("/api/app24005_personal_hub/be/mod01/contact/",json={"user_id":"123","user_name":"guguldash","contact_name": "neha","phone_no": "9871956877","email":"neha@gmail.com","gender_id":"F","gender_name":"Female"}).json()
            new_asset = client.post("/api/app24005_personal_hub/be/mod01/asset/",json={"user_id":"123","user_name":"guguldash","type_id":new_assettype.get("_id"),"type_name": "Laptop","title":"Dell","desc":"Laptop is dell company","purch_date": "2020-03-20","contact_id":new_contact.get("_id"),"contact_name":'Neha',"price":20000,"warantydetail":"From a company or a person to repair or replace a product(1year)","identifier":"VGN-FW550F"}).json()
            response = client.post("/api/app24005_personal_hub/be/mod01/asset/" + str(new_asset.get("_id")), json={"desc": "Laptop is Hp company"})
           
            assert response.status_code == 200
            assert response.json().get("desc") == "Laptop is Hp company"      
            
def test_update_purch_date(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            new_assettype = client.post("/api/app24005_personal_hub/be/mod01/assettype/", json={"user_id":"123","user_name":"guguldash","title": "laptop"}).json()
            new_contact = client.post("/api/app24005_personal_hub/be/mod01/contact/",json={"user_id":"123","user_name":"guguldash","contact_name": "neha","phone_no": "9871956877","email":"neha@gmail.com","gender_id":"F","gender_name":"Female"}).json()
            new_asset = client.post("/api/app24005_personal_hub/be/mod01/asset/",json={"user_id":"123","user_name":"guguldash","type_id":new_assettype.get("_id"),"type_name": "Laptop","title":"Dell","desc":"Laptop is dell company","purch_date": "2020-03-20","contact_id":new_contact.get("_id"),"contact_name":'Neha',"price":20000,"warantydetail":"From a company or a person to repair or replace a product(1year)","identifier":"VGN-FW550F"}).json()
            response = client.post("/api/app24005_personal_hub/be/mod01/asset/" + str(new_asset.get("_id")), json={"purch_date": "2024-07-26"})
           
            assert response.status_code == 200
            assert response.json().get("purch_date") == "2024-07-26"  

def test_update_contact_id(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            new_assettype = client.post("/api/app24005_personal_hub/be/mod01/assettype/", json={"user_id":"123","user_name":"guguldash","title": "laptop"}).json()
            new_contact = client.post("/api/app24005_personal_hub/be/mod01/contact/",json={"user_id":"123","user_name":"guguldash","contact_name": "neha","phone_no": "9871956877","email":"neha@gmail.com","gender_id":"F","gender_name":"Female"}).json()
            new_asset = client.post("/api/app24005_personal_hub/be/mod01/asset/",json={"user_id":"123","user_name":"guguldash","type_id":new_assettype.get("_id"),"type_name": "Laptop","title":"Dell","desc":"Laptop is dell company","purch_date": "2020-03-20","contact_id":new_contact.get("_id"),"contact_name":'Neha',"price":20000,"warantydetail":"From a company or a person to repair or replace a product(1year)","identifier":"VGN-FW550F"}).json()
            response = client.post("/api/app24005_personal_hub/be/mod01/asset/" + str(new_asset.get("_id")), json={"contact_id":"8"})
           
            assert response.status_code == 200
            assert response.json().get("contact_id") == "8"     
                        

def test_update_contact_name(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            new_assettype = client.post("/api/app24005_personal_hub/be/mod01/assettype/", json={"user_id":"123","user_name":"guguldash","title": "laptop"}).json()
            new_contact = client.post("/api/app24005_personal_hub/be/mod01/contact/",json={"user_id":"123","user_name":"guguldash","contact_name": "neha","phone_no": "9871956877","email":"neha@gmail.com","gender_id":"F","gender_name":"Female"}).json()
            new_asset = client.post("/api/app24005_personal_hub/be/mod01/asset/",json={"user_id":"123","user_name":"guguldash","type_id":new_assettype.get("_id"),"type_name": "Laptop","title":"Dell","desc":"Laptop is dell company","purch_date": "2020-03-20","contact_id":new_contact.get("_id"),"contact_name":'Neha',"price":20000,"warantydetail":"From a company or a person to repair or replace a product(1year)","identifier":"VGN-FW550F"}).json()
            response = client.post("/api/app24005_personal_hub/be/mod01/asset/" + str(new_asset.get("_id")), json={"contact_name": "Neha Singh"})
           
            assert response.status_code == 200
            assert response.json().get("contact_name") == "Neha Singh"          
            
def test_update_price(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            new_assettype = client.post("/api/app24005_personal_hub/be/mod01/assettype/", json={"user_id":"123","user_name":"guguldash","title": "laptop"}).json()
            new_contact = client.post("/api/app24005_personal_hub/be/mod01/contact/",json={"user_id":"123","user_name":"guguldash","contact_name": "neha","phone_no": "9871956877","email":"neha@gmail.com","gender_id":"F","gender_name":"Female"}).json()
            new_asset = client.post("/api/app24005_personal_hub/be/mod01/asset/",json={"user_id":"123","user_name":"guguldash","type_id":new_assettype.get("_id"),"type_name": "Laptop","title":"Dell","desc":"Laptop is dell company","purch_date": "2020-03-20","contact_id":new_contact.get("_id"),"contact_name":'Neha',"price":20000,"warantydetail":"From a company or a person to repair or replace a product(1year)","identifier":"VGN-FW550F"}).json()
            response = client.post("/api/app24005_personal_hub/be/mod01/asset/" + str(new_asset.get("_id")), json={"price":40000})
           
            assert response.status_code == 200
            assert response.json().get("price") == 40000     
            
def test_update_warantydetail(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            new_assettype = client.post("/api/app24005_personal_hub/be/mod01/assettype/", json={"user_id":"123","user_name":"guguldash","title": "laptop"}).json()
            new_contact = client.post("/api/app24005_personal_hub/be/mod01/contact/",json={"user_id":"123","user_name":"guguldash","contact_name": "neha","phone_no": "9871956877","email":"neha@gmail.com","gender_id":"F","gender_name":"Female"}).json()
            new_asset = client.post("/api/app24005_personal_hub/be/mod01/asset/",json={"user_id":"123","user_name":"guguldash","type_id":new_assettype.get("_id"),"type_name": "Laptop","title":"Dell","desc":"Laptop is dell company","purch_date": "2020-03-20","contact_id":new_contact.get("_id"),"contact_name":'Neha',"price":20000,"warantydetail":"From a company or a person to repair or replace a product(1year)","identifier":"VGN-FW550F"}).json()
            response = client.post("/api/app24005_personal_hub/be/mod01/asset/" + str(new_asset.get("_id")), json={"warantydetail":"From a company or a person to repair or replace a product(7year)"})
           
            assert response.status_code == 200
            assert response.json().get("warantydetail") == "From a company or a person to repair or replace a product(7year)"      

def test_update_identifier(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            new_assettype = client.post("/api/app24005_personal_hub/be/mod01/assettype/", json={"user_id":"123","user_name":"guguldash","title": "laptop"}).json()
            new_contact = client.post("/api/app24005_personal_hub/be/mod01/contact/",json={"user_id":"123","user_name":"guguldash","contact_name": "neha","phone_no": "9871956877","email":"neha@gmail.com","gender_id":"F","gender_name":"Female"}).json()
            new_asset = client.post("/api/app24005_personal_hub/be/mod01/asset/",json={"user_id":"123","user_name":"guguldash","type_id":new_assettype.get("_id"),"type_name": "Laptop","title":"Dell","desc":"Laptop is dell company","purch_date": "2020-03-20","contact_id":new_contact.get("_id"),"contact_name":'Neha',"price":20000,"warantydetail":"From a company or a person to repair or replace a product(1year)","identifier":"VGN-FW550F"}).json()
            response = client.post("/api/app24005_personal_hub/be/mod01/asset/" + str(new_asset.get("_id")), json={"identifier":"VGN-FW550op"})
           
            assert response.status_code == 200
            assert response.json().get("identifier") == "VGN-FW550op"      
            

#testcase for negative
 
def test_delete_asset_unexisting(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            delete_asset_response = client.delete("/api/app24005_personal_hub/be/mod01/asset/unexisting_id")
            assert delete_asset_response.status_code == 404 

def test_get_asset_unexisting(capsys):
   with TestClient(app) as client:
        with capsys.disabled():
            get_asset_response = client.get("/api/app24005_personal_hub/be/mod01/asset/unexisting_id")
            assert get_asset_response.status_code == 404

