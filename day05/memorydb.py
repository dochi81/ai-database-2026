## 메모리 기반 학생관리 API
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class StudentModel(BaseModel):
    name: str
    age: int
    major: str


## 가짜 데이터 (DB 사용 X)
students = [
    {'id': 1, 'name': '김철수', 'age': 21, 'major': '인공지능'},
    {'id': 2, 'name': '이영희', 'age': 22, 'major': '빅데이터'},
    {'id': 3, 'name': '성유고', 'age': 25, 'major': '컴퓨터공학'}
]


@app.get('/students')
def get_students():
    return students  # 위에 선언한 배열을 그대로 출력

@app.get('/students/{student_id}')
def get_student(student_id:int):
    for student in students:
        if student['id'] == student_id:
            return student
    #404 페이지에러 처리 (예외처리)
    raise HTTPException ( status_code=404, detail= 'Student not found')

# 신규 데이터 추가
@app.post('/students')
def created_student(student: StudentModel):
    #현재 students 배열 최대값+1 새아이디
    new_id = max(item['id'] for item in students) +1


    new_student= { #python 딕셔너리가 json화
        'id': new_id,
        'name': student.name,
        'age': student.age,
        'major': student.major
    }

    students.append (new_student) #id가 추가된 new_student
    return students #배열 전체를 리턴함



