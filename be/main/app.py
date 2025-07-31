import os
from fastapi import FastAPI, Request, Form
from fastapi import FastAPI, Request, Form ,File,UploadFile

from dotenv import load_dotenv
from pymongo import MongoClient
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from datetime import datetime, timedelta
from rubix.be.db import dbconn




load_dotenv()
app = FastAPI()
app.mongodb_client = dbconn
app.dbname = "DB_NAME25014"
app.database = app.mongodb_client[app.dbname]


from store.app25014_professional_hub.be.mod01.account.api import app25014_professional_hub_be_mod01_account_api as app25014_professional_hub_be_mod01_account_api_apiroutes
app.include_router(app25014_professional_hub_be_mod01_account_api_apiroutes, tags=["accoutns"], prefix="/api/app25014_professional_hub/be/mod01/accoutn")


from store.app25014_professional_hub.be.mod01.resource.api import app25014_professional_hub_be_mod01_resource_api as app25014_professional_hub_be_mod01_resource_api_apiroutes
app.include_router(app25014_professional_hub_be_mod01_resource_api_apiroutes,tags=["resources"], prefix="/api/app25014_professional_hub/be/mod01/resource")


from store.app25014_professional_hub.be.mod01.resourcetype.api import app25014_professional_hub_be_mod01_resourcetype_api as app25014_professional_hub_be_mod01_resourcetype_api_apiroutes
app.include_router(app25014_professional_hub_be_mod01_resourcetype_api_apiroutes, tags=["resourcetypes"], prefix="/api/app25014_professional_hub/be/mod01/resourcetype")


from store.app25014_professional_hub.be.mod01.contact.api import app25014_professional_hub_be_mod01_contact_api as app25014_professional_hub_be_mod01_contact_api_apiroutes
app.include_router(app25014_professional_hub_be_mod01_contact_api_apiroutes, tags=["contacts"], prefix="/api/app25014_professional_hub/be/mod01/contact")


from store.app25014_professional_hub.be.mod01.category.api import app25014_professional_hub_be_mod01_category_api as app25014_professional_hub_be_mod01_category_api_apiroutes
app.include_router(app25014_professional_hub_be_mod01_category_api_apiroutes, tags=["categories"], prefix="/api/app25014_professional_hub/be/mod01/category")


from store.app25014_professional_hub.be.mod01.task.api import app25014_professional_hub_be_mod01_task_api as app25014_professional_hub_be_mod01_task_api_apiroutes
app.include_router(app25014_professional_hub_be_mod01_task_api_apiroutes, tags=["tasks"], prefix="/api/app25014_professional_hub/be/mod01/task")



from store.app25014_professional_hub.be.mod01.txn.api import app25014_professional_hub_be_mod01_txn_api as app25014_professional_hub_be_mod01_txn_api_apiroutes
app.include_router(app25014_professional_hub_be_mod01_txn_api_apiroutes, tags=["txns"], prefix="/api/app25014_professional_hub/be/mod01/txn")



from store.app25014_professional_hub.be.mod01.project.api import app25014_professional_hub_be_mod01_project_api as app25014_professional_hub_be_mod01_project_api_apiroutes
app.include_router(app25014_professional_hub_be_mod01_project_api_apiroutes, tags=["projects"], prefix="/api/app25014_professional_hub/be/mod01/project")



@app.get("/ProfessionalHub")
async def goto_main(request: Request): 
    print("mssg hello professionalhub")
    # return RedirectResponse('/app00/fe/main/web/index.htm')
    return RedirectResponse('store/index.htm')
    