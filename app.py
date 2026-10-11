from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import csv

app = FastAPI()

# Enable CORS for GET requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Read the CSV file from the same directory
CSV_FILE = Path(__file__).resolve().parent / "students.csv"

with open(CSV_FILE, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    students = [
        {
            "studentId": int(row["studentId"]),
            "class": row["class"]
        }
        for row in reader
    ]


@app.get("/api")
def get_students(
    class_filter: list[str] | None = Query(default=None, alias="class")
):
    # Return all students if no class filter is provided
    if class_filter is None:
        filtered_students = students
    else:
        selected_classes = set(class_filter)

        # Preserve the original CSV row order
        filtered_students = [
            student for student in students
            if student["class"] in selected_classes
        ]

    return {"students": filtered_students}