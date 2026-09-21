## FASTAPI 다시
from fastapi import FastAPI
from pydantic import BaseModel

app= FastAPI() #API 서버시작

## 클래스: 함수의 변형, 현재는 데이터 구조만
# 데이터 제대로 입력 검증

class StudentModel(BaseModel):
    name: str # 문자열
    email: str #문자열
    age: int #숫자
    major: str  |None = None # 문자열


@app.get('/')  #데코레이션
def read_root():
    return {'message':'Hello FastAPI'}


@app.get('/students')
def get_students():
    return [
        {'id':1,"name":"김철수","major":"인공지능"},
        {'id':1,"name":"이영희","major":"데이터분석"},
        {'id':1,"name":"성유고","major":"컴퓨터공학"},
    ]

@app.get ('/students/{id}')
def get_student(id:int):
    return {'student_id':id}

@app.get('/search')
def search_student(major: str | None = None):
    return {'major':major}

@app.post('/students')
def creat_students(student:StudentModel):
    return {
            'message':'학생등록',
            'data':student
            }


@app.patch('/student/{id}')
def update_student(id:int):
    return {'message':f'{id}번 학생 수정'}

@app.delete('/student/{id}')
def delet_student(id:int):
    return {'message':f'{id}번 학생 삭제'}