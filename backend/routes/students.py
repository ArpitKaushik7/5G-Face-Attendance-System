from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import os

router = APIRouter()
EXCEL_PATH = r"E:\\5G Face Attendance System\\form_responses.xlsx"

class Student(BaseModel):
    Id: str
    Name: str
    Branch: str
    Batch: str

@router.post("/addStudents")
def add_student(student: Student):
    try:
        df = pd.read_excel(EXCEL_PATH)

        if student.Id in df["Id"].astype(str).values:
            raise HTTPException(status_code=400, detail="Student ID already exists")

        new_row = {
            "Timestamp": pd.Timestamp.now(),
            "Email Address": "",
            "Id": student.Id,
            "Name": student.Name,
            "Branch": student.Branch,
            "Photo (name it as ID_Firstname Surname)": "",
            "Batch": student.Batch
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_excel(EXCEL_PATH, index=False)
        return {"message": "Student added successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
