

## FASTAPI 다시
from fastapi import FastAPI

app= FastAPI() #API 서버시작
@app.get('/hi')
def read_hi():
    return {'message':'Hello FastAPI'}
