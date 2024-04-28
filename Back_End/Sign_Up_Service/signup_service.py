# signup_service.py

'''from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Database Connection
DATABASE_URL = "mysql+mysqlconnector://root:Omm@ir510219900@127.0.0.1/cloud_assignment"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# User Model
class User(Base):
    __tablename__ = "signup_data"
    id = Column(String, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)

# Routes
@app.post("/signup/")
async def signup_user(first_name: str, last_name: str, email: str):
    db = SessionLocal()
    user = User(first_name=first_name, last_name=last_name, email=email)
    db.add(user)
    db.commit()
    db.close()
    return {"message": "User signed up successfully"}'''

#------------------------------------------Previous Code-------------------------------------------------------#
from fastapi import FastAPI, Response
from pydantic import BaseModel
from mysql_connection import *

app = FastAPI()

class SignUp(BaseModel):
    first_name:str
    last_name:str
    dob:str
    email_reg:str
    hashed_password:str

@app.get('/')
def home():
    return 'Welcome to App'

@app.post('/signup')
def sign_up(request:SignUp):
    print("REQ RECEIVED")
    print(request)
    try:
        parameters = (request.first_name,request.last_name,request.dob,request.email_reg,request.hashed_password)
        cur.execute("""
                        INSERT INTO users_db (first_name, last_name, dob, email, password)
                        VALUES (%s, %s, %s, %s, %s);
                        """, parameters)
                    
        connection.commit()
        print("SUCCESS")
        return Response(content="Signup Successful", status_code=201)
    except:
        print("FAIL")
        return Response(content="Signup Unsuccessful", status_code=400)
