from fastapi import FastAPI,Path,HTTPException,Query
import json
app=FastAPI()

# Helper funcion
def load_data():
    with open('package.json', 'r') as f:
        data=json.load(f)
    return data 

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
    sort_order=True if sort_order=='desc' else False
    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)
    return sorted_data