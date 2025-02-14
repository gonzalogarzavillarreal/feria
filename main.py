from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import json
from bson import BSON
from bson import ObjectId
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = [
    "http://localhost:8000/",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
password=os.getenv('passMongo')
uri = f"mongodb+srv://BotsIA:{password}@asistentes.fnina.mongodb.net/?retryWrites=true&w=majority&appName=Asistentes"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.Feria
# Modelo de datos
class registro(BaseModel):     
    id: str
    equipo: str
    fecha: str
    proyecto:str
    representante:str
    carrera:str
    tetra:str
    turno:str 
    asesor:str
    asesorSecundario:str
    descripcionProyecto:str
    recursos:str
    

# Obtener un usuario por ID
@app.get("/registros/{id}",response_model=registro)
def get_registro(id: str):
     collection = db.Registros
     object_id = ObjectId(id)
     registroNew = collection.find_one({"_id":object_id})
     registroResponse={}
     registroResponse["id"] = id
     registroResponse["equipo"]=registroNew["equipo"]
     registroResponse["fecha"]=registroNew["fecha"]
     registroResponse["proyecto"]=registroNew["proyecto"]
     registroResponse["representante"]=registroNew["representante"]
     registroResponse["carrera"]=registroNew["carrera"]
     registroResponse["tetra"]=registroNew["tetra"]
     registroResponse["turno"]=registroNew["turno"]
     registroResponse["asesor"]=registroNew["asesor"]
     registroResponse["asesorSecundario"]=registroNew["asesorSecundario"]
     registroResponse["descripcionProyecto"]=registroNew["descripcionProyecto"]
     registroResponse["recursos"]=registroNew["recursos"]

     response={
        "success":True,
        "regsitro":registroResponse
     }


     return JSONResponse(status_code=200, content=response)

    
# Agregar un nueva demanda
@app.post("/registros", response_model=registro)
def create_Registro(registros: registro):
    collection = db.Registros
    new_Registro = registros.model_dump(by_alias=True,exclude={"id"})  # Convert model to dict
    result =  collection.insert_one(new_Registro)  # Insert into MongoDB
    object_id = result.inserted_id  # Esto es de tipo ObjectId
    registros.id = str(object_id)
    responseRegistro=registros.model_dump(by_alias=True)
    response={
        "success":True,
        "registro":responseRegistro
    }
    return JSONResponse(status_code=200, content=response)