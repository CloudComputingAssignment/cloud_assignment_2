from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymysql
from datetime import datetime, timedelta
import hashlib

app = FastAPI()

# Pydantic models for request bodies
class LoginForm(BaseModel):
    email: str
    password: str

class ResetPasswordForm(BaseModel):
    email: str

# Database connection setup
def get_connection():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="Omm@ir510219900",
        database="cloud_assignment",
        cursorclass=pymysql.cursors.DictCursor
    )

def hash_password(password):
    # Use a secure hashing algorithm such as SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

# API endpoint for user login
@app.post("/signin")
def login(form: LoginForm):
    connection = get_connection()
    with connection.cursor() as cursor:
        hashed_password = hash_password(form.password)
        cursor.execute(
            'SELECT * FROM users_db WHERE email = %s AND password = %s',
            (form.email, hashed_password)
        )
        print (form.email)
        user = cursor.fetchone()

        if user:
            return {"message": "Login successful", "user": user}
        else:
            raise HTTPException(status_code=401, detail="Invalid email or password")

# API endpoint for resetting password
@app.post("/reset-password")
def reset_password(form: ResetPasswordForm):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM users_db WHERE email = %s', (form.email,))
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="Email not found")

        reset_token = generate_reset_token()
        reset_expiration = datetime.now() + timedelta(hours=1)

        cursor.execute('''
            UPDATE users_db
            SET reset_token = %s, reset_expiration = %s
            WHERE email = %s
        ''', (reset_token, reset_expiration, form.email))
        connection.commit()

        send_reset_email(form.email, reset_token)

        return {"message": "Password reset email sent"}

# Helper functions (replace with your actual implementations)
#def hash_password(password):
   # return hashlib.sha256(password.encode()).hexdigest()
   # return password  # Implement your password hashing logic

def generate_reset_token():
    return "sample_reset_token"  # Implement your token generation logic

def send_reset_email(email, reset_token):
    print(f"Reset email sent to {email} with token {reset_token}")  # Implement your email sending logic

# Run the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
