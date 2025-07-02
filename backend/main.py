from fastapi import FastAPI
from routes import students, attendance

app = FastAPI()

app.include_router(students.router)
app.include_router(attendance.router, prefix="/attendance")
