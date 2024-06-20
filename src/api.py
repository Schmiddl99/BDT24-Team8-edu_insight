from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class FormData(BaseModel):
    Entry_T_ID: int
    Student_P_ID: int
    DisplayName: str
    sex: bool
    address: bool
    famsize: bool
    Pstatus: bool
    Medu: int
    Fedu: int
    traveltime: Optional[int] = None
    studytime: Optional[int] = None
    failures: int
    schoolsup: bool
    famsup: bool
    activities: bool
    romantic: bool
    famrel: int
    freetime: int
    goout: int
    Dalc: int
    Walc: int
    health: int

@app.post("/submit_form")
async def submit_form(form_data: FormData):
    # Here you can implement the logic to store the form data, analyze it, and provide personalized recommendations
    print(f"Received form data: {form_data}")
    return {"message": "Form data received successfully"}

@app.get("/")
async def root():
    return {"message": "FastAPI is running"}
