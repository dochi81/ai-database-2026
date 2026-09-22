# day05 main.py , memory.py와 동일 +DB처리 추가
import uvicorn
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel 


# 우리가 만든 database.py
from database import get_connection
from psycopg.rows import dict_row

app = FastAPI(title='FastAPI DB연동')
# 파일탐색기 들어가서 해당 마우스 오른쪽 클릭 터미널 열기 
# uvicorn app:main --reload --port 8000 실행
# http://127.0.0.1:8000/docs 적기 연동된 웹 브라우저 열기

# 학생모델

class StudentModel(BaseModel):
    name: str
    email:str |None =None 
    age:int | None= None
    major: str

# 전체학생 조회
@app.get ('/students')
def get_students():

    # 실제 db 연결
    conn = get_connection()
    cursor = conn.cursor(row_factory =dict_row) # 마우스커서처럼 테이블 한행씩 가리키는 값


    try:
        # 실제 쿼리는 dbeaver 등에서 작성 확인하고 복사해옴
        cursor.execute("""
            select id, name, email, age, major, created_at
                from students
               order by id
        """)
        # 위 쿼리를 실행해서 데이터 다 가져와 students에 할당
        students = cursor.fetchall()

        if students is None:
           #특정 학생이 정보가 없으면 404에러 발생
           raise HTTPException (status_code=404, detail='Student not found')
           
        return students
    
    # except Exception: #예외

    finally: # 예외 여부 관계없이 항상 실행

        cursor.close() # 커서도 닫아줌
        conn.close() # 예외가 발생하든 안하든 무조건 DB연결 닫아야함


# 한명 조회
@app.get('/students/{id}')
def get_student(id:int):
    conn = get_connection()
    cursor = conn. cursor(row_factory=dict_row)


    try:
        #쿼리 실행, 외부에서 받는 값은 %s로 변경, 값은 (id,)형식으로 작성
        cursor.execute("""
        select id, name, email, age, major, created_at
        from students
        where id = %s 
        """,(id,))


        student = cursor.fetchone() #커서에서 1건만 가져옴
        if student is None:
            raise HTTPException (status_code=404, detail= 'Student not found')

        return student
    finally:
       cursor.close() #접속 종료전에 커서를 닫아야함
       conn.close()

# 학생등록
@app.post('/students')
def create_student(student:StudentModel):
    conn = get_connection()
    cursor = conn.cursor(row_factory=dict_row)

    try:
        # %d는 사용불가
        cursor.execute("""
            insert into students (name, email, age, major)
            values (%s, %s, %s, %s); 
        """, (student.name, student.email, student.age, student.major))

        # new_student = cursor.fetchone() #새로 DB에 등록된 학생정보
        conn.commit() # 커밋

        return {'message':'Student registration done'}
    
    
    except:
        conn.rollback() #롤백
        raise

    finally:
        cursor.close()
        conn.close()

# 수정,patch 일부 수정은 거의 사용안함
@app.put ('/students/{id}')
def update_student(id: int, student: StudentModel):
    conn = get_connection()
    cursor = conn.cursor(row_factory=dict_row)


    try:
        cursor.execute("""
        update students set
        name= %s,
        age= %s,
        email= %s,
        major= %s
        where id= %s
        returning id, name, email, age, major, created_at
        """,(student.name, student.age,student.email,student.major,id))


        # 변수
        updated_student = cursor.fetchone()
        
        if update_student is None:
            conn.rollback()
            raise HTTPException(status_code=404, detail='Studentnot found')

        conn.commit() # 빼면 안됨
        return updated_student

    except:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()    

# 삭제
@app.delete('/students/{id}')
def delete_student(id:int):
    conn = get_connection()
    cursor = conn.cursor(row_factory=dict_row)

    try:
        cursor.execute("""
                delete from students
                where id =%s
                returning id,name
        """,(id,))

        deleted_student =cursor.fetchone()

        if deleted_student is None:
            conn.rollback()
            raise HTTPException(status_code=404,detail='Student not found')

        conn.commit()
        return {
        'message':'student deleted',
        'student': deleted_student
        }
 
    except:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()



# 디버깅시 추가할 것
# 디버깅 잘하려면 구구단 디버깅 해볼것


if __name__ == '__main__':

    uvicorn.run(
        'main_debug:app',
        host='127.0.0.1',
        port=8000, # 디버깅용 포트 변경
        reload=True,
        log_level='debug'
    )

        