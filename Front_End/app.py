# app.py (Streamlit)

import streamlit as st
import requests
from sqlalchemy.exc import IntegrityError
from hashpassword import hash_password
#from session_state import SessionState # Ensure you have session_state.py in your project directory


from reset_password import send_reset_email,generate_reset_token

from datetime import datetime, timedelta
import pandas as pd
import mysql.connector
import csv
import pandas as pd
import numpy as np
from home import about

config={'host':'127.0.0.1',
        'user':'root', 'password':'Omm@ir510219900',
                              
        'database':'cloud_assignment'}

# Establish a connection
connection = mysql.connector.connect(**config)
cur = connection.cursor()

def get_session_state():
    if 'user' not in st.session_state:
        st.session_state.user = None
    return st.session_state

def datamgmt ():
    st.title("Data Management Service")
    uploaded_file = st.file_uploader("Upload CSV File")

    if uploaded_file is not None:
        if st.button("Upload"):
            # Send file to backend API
            files = {"file": uploaded_file}
            response = requests.post("http://localhost:8003/upload", files=files)

            if response.status_code == 200:
                file_info = response.json()
                st.success(f"File uploaded successfully: {file_info['file_name']}")
            else:
                st.error("Failed to upload file")


def user_dashboard():
    st.title("User Dashboard")
    st.subheader("User Details")

    user = st.session_state.user
    st.write(f"First Name: {user['first_name']}")
    st.write(f"Last Name: {user['last_name']}")
    st.write(f"Email: {user['email']}")
    st.write(f"Date of Birth: {user['dob']}")

    st.subheader("Update User Details")

    change_first_name = st.checkbox("Want to change your First Name?")

    if change_first_name:
        changefname = st.text_input("Enter your new First Name")
        
        changeb = st.button("Change First Name")
        if changeb:
            cur.execute('''
            UPDATE users_db
            SET first_name = %s
            WHERE id = %s
            ''', (changefname,st.session_state.user['id']))
            connection.commit()
            st.success("Updated Successfully")

    change_last_name = st.checkbox("Want to change your Last Name?")

    if change_last_name:
        changelname = st.text_input("Enter your new Last Name")
        changel = st.button("Change Last Name")
        if changel:
            cur.execute('''
            UPDATE users_db
            SET last_name = %s
            WHERE id = %s
            ''', (changelname,st.session_state.user['id']))
            connection.commit()
            st.success("Updated Successfully")

    change_first_name = st.checkbox("Want to change your DOB?")

    if change_first_name:
        changedob = st.text_input("Enter your new Date of Birth (YYYY-MM-DD)")
        
        changed = st.button("Change DOB")
        if changed:
            cur.execute('''
            UPDATE users_db
            SET dob = %s
            WHERE id = %s
            ''', (changedob,st.session_state.user['id']))
            connection.commit()
            st.success("Updated Successfully")


    st.subheader("Actions")
    passbutton = st.checkbox("Change Password")

    if passbutton:
        oldpass = st.text_input("Enter your old password", type="password")
        newpass = st.text_input("Enter your new password", type="password")
        connpass = st.text_input("Confirm your new password", type="password")
        changep = st.button("Change")
        if changep:
            if hash_password(oldpass) != st.session_state.user[5]:
                st.error("Old password doesn't match")
            else:
                if newpass != connpass:
                    st.error("New and Confirm password don't match")
                else:
                    hashpass = hash_password(newpass)
                    cur.execute('''
                    UPDATE users_db
                    SET password = %s
                    WHERE id = %s
                    ''', (hashpass,st.session_state.user['id']))
                    connection.commit()
                    st.success("Password Updated Successfully")

def File():
    st.title("File Upload")

    # File upload widget
    uploaded_file = st.file_uploader("Choose a CSV file (Max 10MB)", type="csv", accept_multiple_files=False)

    if uploaded_file is not None:
        if st.button("Upload"):
            try:
                # Prepare file for upload
                files = {"file": uploaded_file}

                # Make POST request to API endpoint
                response = requests.post("http://localhost:8003/upload", files=files)

                if response.status_code == 200:
                    # Display success message
                    file_info = response.json()
                    st.success(f"File uploaded successfully: {file_info['file_name']}")
                else:
                    # Display error message
                    st.error("Failed to upload file")
            
            except Exception as e:
                st.error(f"Failed to upload file: {str(e)}")

def signup():

    st.header('Create a new Account')
    first_name = st.text_input('Enter your First Name:')
    last_name = st.text_input("Enter your Last Name:")
    dob = st.text_input('Enter your DOB(YYYY-MM-DD):', placeholder="01/01/1980")
    email_reg = st.text_input('Enter your email account:', placeholder="abc123@gmail.com")
    password_reg = st.text_input('Enter your password:', type="password")
    confirm_password = st.text_input('Confirm your password:', type="password")
    register=st.button('Register')

    if register == True:
        if password_reg != confirm_password:
            st.error('Passwords do not match. Please try again.')
        
        elif not email_reg.endswith('@gmail.com'):
            st.error('Please register with a Gmail account.')
        else:
            hashed_password = hash_password(password_reg)

            try:
                parameters = {"first_name":first_name,"last_name":last_name,"dob":dob,"email_reg":email_reg,"hashed_password":hashed_password}
                response = requests.post('http://localhost:8001/signup',json=parameters)
                status_code = response.status_code
                if status_code == 201:
                     st.success(f"Registration succesful for {email_reg}!")
                else:
                     st.error(f'Registration Unsuccessful')
            
            except IntegrityError:
                    st.error(f"Email {email_reg} is already registered. Please use a different email.")
  
def user_signin():
    st.header('User Login')
    email_login = st.text_input('Enter your email:', key='email_input')
    password_login = st.text_input('Enter your Password:', key='password_input', type="password")

    if st.button("Login"):
        response = requests.post("http://localhost:8000/signin", json={"email": email_login, "password": password_login})
        if response.status_code == 200:
            data=response.json()
           # user = data['user']
            st.success("Login successful.")
            st.session_state.user = response.json()['user']
        
            st.session_state.logged_in = True 
            
        else: st.error ("Incorrect login details")

# Streamlit UI for password reset
def forgot_password():
    st.header('Forgot Password')
    email_forgot = st.text_input("Enter your registered Gmail account:")

    if st.button("Reset Password"):
        response = requests.post("http://localhost:8000/reset-password", json={"email": email_forgot})
        if response.status_code == 200:
            st.success("Password reset email sent.")
        else:
            st.error("Email not found. Please enter a registered Gmail account.")
def upload_data(file):
    # Check if file is uploaded
    if file is None:
        st.error("Please upload a CSV file.")
        return

    # Check file size
    if file.size > 10*1024*1024:  # 10MB limit
        st.error("File size exceeds the limit (10MB). Please upload a smaller file.")
        return
    
    # Read uploaded file
    df = pd.read_csv(file)
    
    # Perform further processing and data upload
    # (Your code for processing and uploading data goes here)

    st.success("Data uploaded successfully!")
def window_screen():
    user_input = st.radio('Please select an option:', options=['Sign In', 'Sign Up', 'Admin Sign In'], horizontal=True)
    if user_input == 'Sign In':
        user_signin()
        if get_session_state().user:
            if get_session_state().user['email'] == 'admin@gmail.com':  # Check if the user is admin
                admin_dashboard()
                
            else:
                user_dashboard()
                #st.subheader("Upload Data File (Limit: 10MB per file)")
                #uploaded_file = st.file_uploader("Choose a CSV file (Max 10MB)", type="csv", accept_multiple_files=False)
                
                #datamgmt()
                File()

                #upload_data(uploaded_file)
    
    elif user_input == 'Sign Up':
        signup()
    
    elif user_input == 'Admin Sign In':
        admin_sign_in()
def admin_dashboard():
    st.title("Admin Dashboard")
    st.subheader("User Details")

    # Fetch all users from the database
    cur.execute("SELECT * FROM users_db")
    all_users = cur.fetchall()

    # Display user information and allow admin to make changes
    for user in all_users:
        st.write(f"ID: {user[0]}")
        st.write(f"First Name: {user[1]}")
        st.write(f"Last Name: {user[2]}")
        st.write(f"Email: {user[3]}")
        st.write(f"Date of Birth: {user[4]}")

        st.subheader("Let Update User Details------------------")

        change_first_name = st.checkbox(f"Change First Name for User {user[0]}")

        if change_first_name:
            new_first_name = st.text_input(f"Enter new First Name for User {user[0]}")
            changeb = st.button("Change First Name")
            if changeb:
                cur.execute('''
                UPDATE users_db
                SET first_name = %s
                WHERE id = %s
                ''', (new_first_name, user[0]))
                connection.commit()
                st.success("Updated Successfully")
                #log_activity(f"Changed First Name for User {user[0]}")

        change_last_name = st.checkbox(f"Change Last Name for User {user[0]}")

        if change_last_name:
            new_last_name = st.text_input(f"Enter new Last Name for User {user[0]}")
            changel = st.button("Change Last Name")
            if changel:
                cur.execute('''
                UPDATE users_db
                SET last_name = %s
                WHERE id = %s
                ''', (new_last_name, user[0]))
                connection.commit()
                st.success("Updated Successfully")
               # log_activity(f"Changed Last Name for User {user[0]}")

        change_dob = st.checkbox(f"Change Date of Birth for User {user[0]}")

        if change_dob:
            new_dob = st.text_input(f"Enter new Date of Birth for User {user[0]} (YYYY-MM-DD)")
            changed = st.button("Change DOB")
            if changed:
                cur.execute('''
                UPDATE users_db
                SET dob = %s
                WHERE id = %s
                ''', (new_dob, user[0]))
                connection.commit()
                st.success("Updated Successfully")
               # log_activity(f"Changed Date of Birth for User {user[0]}")

        st.subheader("Actions")
        passbutton = st.checkbox(f"Change Password for User {user[0]}")

        if passbutton:
            oldpass = st.text_input("Enter the old password", type="password")
            newpass = st.text_input("Enter the new password", type="password")
            connpass = st.text_input("Confirm the new password", type="password")
            changep = st.button("Change")
            if changep:
                if hash_password(oldpass) != user[5]:
                    st.error("Old password doesn't match")
                else:
                    if newpass != connpass:
                        st.error("New and Confirm password don't match")
                    else:
                        hashpass = hash_password(newpass)
                        cur.execute('''
                        UPDATE users_db
                        SET password = %s
                        WHERE id = %s
                        ''', (hashpass, user[0]))
                        connection.commit()
                        st.success("Password Updated Successfully")
                       # log_activity(f"Changed Password for User {user[0]}")

        # Provide option to deactivate or activate user
        st.subheader("Change User Status")
        toggle_status = st.radio(f"Toggle Status for User {user[0]}", options=["Activate", "Deactivate"])
        if st.button(f"{toggle_status} User {user[0]}"):
            new_status = 1 if toggle_status == "Activate" else 0
            cur.execute('''
            UPDATE users_db
            SET status = %s
            WHERE id = %s
            ''', (new_status, user[0]))
            connection.commit()
            st.success(f"User {user[0]} {toggle_status.lower()}d successfully")
            #log_activity(f"{toggle_status} User {user[0]}")

        st.write('---')
def admin_sign_in():
    st.header('Admin Login')
    email_login = st.text_input('Enter your email:', placeholder="admin@gmail.com")
    password_login = st.text_input('Enter your Password:', placeholder="Password", type="password")
    
    if st.button("Admin Login"):
        # Authenticate admin credentials
        if email_login == 'admin@gmail.com' and password_login == 'malik123':  # Replace with actual admin credentials
           
            st.success("Admin Login successful.")
            admin_dashboard()
        else:
            st.error("Invalid email or password.")

def main():
    st.title("User Authentication")
   # signup()

    #st.header('User Login')
    #user_signin()
    #forgot_password()
    #upload_data()
    #user_dashboard()
    st.title("Cloud Based Web Storage App")


    st.sidebar.title("Menu")
    app_mode = st.sidebar.selectbox('Get Started:', ['User', 'Home'])

    if app_mode == 'User':
        window_screen()
        
        

    #elif app_mode == 'About':
     #   about()
        
        
    else:
       about()
    
if __name__ == "__main__":
    main()
