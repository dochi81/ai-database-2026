<<<<<<< HEAD
#파이썬에서 다른 패키지를 사용하려면
# from *import **
#import*
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def read_root():
    return{'message':'Hello FastAPI'}
=======
# 파이썬에서 다른 패키지를 사용하려면
# from * import **
# import * 
from fastapi import FastAPI

app = FastAPI()  

@app.get('/')
def read_root():
    return { 'message' : 'Hello FastAPI' }
>>>>>>> 5140674c3b177a8d7f2d5a1e11d975968ead3cf5
