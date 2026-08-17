from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal
import json
app=FastAPI()

class Patient(BaseModel):
    id:Annotated[str,Field(...,description="Id of the patient",examples="P001")]
    name: Annotated[str,Field(...,description="Name of the patient")]
    city: Annotated[str,Field(...,description="Name of the city")]
    age: Annotated[str,Field(...,gt=0,lt=120,description="Age of the patient")]
    gender: Annotated[Literal["male","female","others"],Field(...,description="Gender of the patient")]
    height: Annotated[float,Field(...,gt=0,description="Height of the patient in meters")]
    weight: Annotated[float,Field(...,gt=0,description="Weight of the patient in kgs")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi=self.weight/(self.height**2)
        return bmi
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi <18.5:
            return "Underweight"
        elif self.bmi<25:
            return "Normal"
        elif self.bmi<30:
            return "Normal"
        else:
            return "Obese"
# Helper funcion
def load_data():
    with open('package.json', 'r') as f:
        data=json.load(f)
    return data 

def save_data(data):
    with open('package.json','w') as f:
        json.dump(data,f)

@app.get("/")
def hello():
    return {"message": "Hello, World!"}

@app.get("/about")
def about():
    return {"message": "This is about section"}

@app.get("/view")
def view():
    data=load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str= Path(...,description='Id of the patient',example='P001')):
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail="Patient not found")

@app.get("/sort")
def sirt_patients(sort_by: str=Query(...,description='sort on the basis of height,weight or bmi'),order: str=Query("asc",description='sort on asc or desc order')):
    valid_parameters=["height","weight","bmi"]
    if sort_by not in valid_parameters:
        raise HTTPException(status_code=400,detail=f"Invalide field select between these {valid_parameters}")
    if order not in ["asc","desc"]:
        raise HTTPException(status_code=400,detail="select between asc or dec")
    data=load_data()
    sort_order=True if order=='desc' else False
    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order) 
    return sorted_data

@app.post('/create')
def create_patient(patient:Patient):

    #load existing data
    data=load_data()
    #Check if the patient already exist
    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient already exist')
    #New patient add to the database
    data[patient.id]=patient.model_dump(exclude=['id'])
    #Save in to json file
    save_data(data)
    return JSONResponse(status_code=201,content={'message':'Patient created successfully'})