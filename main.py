from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI()

DATA_FILE = "courses.json"


def init_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

init_file()


def add_to_json(new_course: dict):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    data.append(new_course)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_courses():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


class Course(BaseModel):
    course_name: str
    year: str
    semester: str
    grade: str

@app.get("/courses")
def get_courses():
    try:
        courses = load_courses()
        return courses
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 읽기 오류: {str(e)}")


@app.post("/courses")
def add_course(course: Course):
    try:
        add_to_json(course.model_dump())
        return {"message": "과목이 추가되었습니다.", "course": course}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"저장 오류: {str(e)}")