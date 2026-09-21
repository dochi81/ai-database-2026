## FASTAPI 다시
from fastapi import FastAPI

app= FastAPI() #API 서버시작
@app.get('/')
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
