def create_table():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Omm@ir510219900",
            database="cloud_assignment"
        )
        
        cursor = connection.cursor()
        create_table_query = """
            CREATE TABLE IF NOT EXISTS uploaded_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_name VARCHAR(255),
                upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                column1 VARCHAR(255),
                column2 VARCHAR(255),
                column3 VARCHAR(255),
                -- Add additional columns as needed
                UNIQUE KEY unique_file_row (file_name, upload_time)
            )
        """
        cursor.execute(create_table_query)
        print("Table created successfully")
        
        cursor.close()
        connection.close()
    except mysql.connector.Error as e:
        print(f"Error creating table: {e}")

# Call the create_table function to execute the SQL command
create_table()
def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Omm@ir510219900",
            database="cloud_assignment"
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None


import pandas as pd

def insert_csv_data_to_mysql(connection, table_name, file_name, csv_file):
    try:
        cursor = connection.cursor()

        # Read CSV file into DataFrame
        df = pd.read_csv(csv_file)

        # Insert each row into MySQL table with file_name and upload_time
        for index, row in df.iterrows():
            query = f"INSERT INTO {table_name} (file_name, column1, column2, column3) VALUES (%s, %s, %s, %s)"
            values = (file_name, row['column1'], row['column2'], row['column3'])
            cursor.execute(query, values)

        connection.commit()
        cursor.close()
        print(f"CSV data from {file_name} inserted into MySQL successfully")
        return True
    except Exception as e:
        print(f"Error inserting CSV data into MySQL: {e}")
        connection.rollback()
        return False


def upload_and_save_to_mysql(connection, table_name):
    uploaded_files = st.file_uploader("Upload CSV File(s)", type="csv", accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_name = uploaded_file.name
            if st.button(f"Save {file_name} to MySQL"):
                try:
                    if insert_csv_data_to_mysql(connection, table_name, file_name, uploaded_file):
                        st.success(f"CSV data from {file_name} saved to MySQL successfully!")
                    else:
                        st.error(f"Failed to save CSV data from {file_name} to MySQL.")
                except Exception as e:
                    st.error(f"Error processing file {file_name} and saving to MySQL: {e}")
    return uploaded_files

def load_csv_to_mysql(csv_file_path, table_name):
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Omm@ir510219900",
            database="cloud_assignment"
        )

        cursor = connection.cursor()
        load_query = f"""
            LOAD DATA INFILE '{csv_file_path}'
            INTO TABLE {table_name}
            FIELDS TERMINATED BY ','
            ENCLOSED BY '"'
            LINES TERMINATED BY '\n'
            IGNORE 1 LINES
        """
        cursor.execute(load_query)
        connection.commit()
        print("CSV data loaded into MySQL table successfully")
    except mysql.connector.Error as e:
        print(f"Error loading CSV data into MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()




    # Connect to MySQL database
    connection = connect_to_mysql()
    if connection is None:
        st.error("Failed to connect to MySQL database. Check connection settings.")
        return

    # Define MySQL table name
    table_name = 'uploaded_data'

    # Upload and save multiple CSV files to MySQL
    csv_file_path=upload_and_save_to_mysql(connection, table_name)

    # Close database connection when app exits
   # connection.close()
    #csv_file_path = 
    table_name = 'uploaded_data'
    load_csv_to_mysql(csv_file_path, table_name)

def upload_data():
    st.header("Upload CSV File")
    uploaded_file = st.file_uploader("Choose a CSV file (Max 10MB)", type="csv", accept_multiple_files=False)

    if uploaded_file is not None:
        if st.button("Process File"):
            # Check if user is logged in before processing file
            if 'logged_in' in st.session_state and st.session_state.logged_in:
                # Process the uploaded file
                try:
                    df = pd.read_csv(uploaded_file)
                    st.success("File uploaded successfully!")
                    st.write(df)  # Display the DataFrame
                    # Add your code for further processing and data upload
                except Exception as e:
                    st.error(f"Error processing file: {e}")
            else:
                st.error("Please log in to upload and process files.")


# Helper function to fetch user data from backend
def fetch_user_data(email, password):
    response = requests.post("http://localhost:8000/signin", json={"email": email, "password": password})
    if response.status_code == 200:
        return response.json()['user']
    else:
        return None

def dashboard():
    st.title("User Authentication and Dashboard")

    # Initialize session state variables
    if 'user' not in st.session_state:
        st.session_state.user = None
        st.session_state.logged_in = False

    # Display sign-in form if user is not logged in
    if not st.session_state.logged_in:
        st.header('User Login')
        email_login = st.text_input('Enter your email:', key='email_input')
        password_login = st.text_input('Enter your Password:', key='password_input', type="password")

        if st.button("Login"):
            user_data = fetch_user_data(email_login, password_login)
            if user_data:
                st.success("Login successful.")
                st.session_state.user = user_data
                st.session_state.logged_in = True
            else:
                st.error("Incorrect login details")

    # Display user dashboard if user is logged in
    if st.session_state.logged_in:
        st.header("User Dashboard")
        user = st.session_state.user

        if user:
            st.subheader("User Details")
            st.write(f"First Name: {user['first_name']}")
            st.write(f"Last Name: {user['last_name']}")
            st.write(f"Email: {user['email']}")
            st.write(f"Date of Birth: {user['dob']}")

            st.subheader("Update User Details")

            change_first_name = st.checkbox("Want to change your First Name?")
            if change_first_name:
                new_first_name = st.text_input("Enter your new First Name")
                if st.button("Change First Name"):
                    # Update first name in backend database (replace with actual update logic)
                    st.success("First Name updated successfully.")

            change_last_name = st.checkbox("Want to change your Last Name?")
            if change_last_name:
                new_last_name = st.text_input("Enter your new Last Name")
                if st.button("Change Last Name"):
                    # Update last name in backend database (replace with actual update logic)
                    st.success("Last Name updated successfully.")

            st.subheader("Upload Data File")
            uploaded_file = st.file_uploader("Choose a file")
            if uploaded_file is not None:
                # Process the uploaded file (e.g., save to database)
                st.success("File uploaded successfully.")

            st.subheader("Change Password")
            old_password = st.text_input("Enter your old password", type="password")
            new_password = st.text_input("Enter your new password", type="password")
            confirm_password = st.text_input("Confirm your new password", type="password")
            if st.button("Change Password"):
                if old_password != user['password']:
                    st.error("Old password doesn't match")
                elif new_password != confirm_password:
                    st.error("New and Confirm password don't match")
                else:
                    # Update password in backend database (replace with actual update logic)
                    st.success("Password updated successfully.")
        else:
            st.error("User details not found. Please log in.")



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

def user_dashboard():
    #if 'logged_in' not in st.session_state:
     #   st.warning("Please login to access this page.")
      #  return 
    st.title("User Dashboard")
    st.subheader("User Details")
    #user = st.session_state.user
   
    #st.write(f"first_name: {user['first_name']}")
    #st.write(f"last_name: {user['last_name']}")
    #st.write(f"email: {user['email']}")
    #st.write(f"dob: {user['dob']}")

    user = st.session_state.user
    st.write(f"First_name: {user['first_name']}")
    st.write(f"last_name: {user['last_name']}")
    st.write(f"email: {user['email']}")
    st.write(f"dob: {user['dob']}")

    st.subheader("Update User Details")

    change_first_name = st.checkbox("Want to change your First Name?")

    if change_first_name:
        print ('change first name working')
        changefname = st.text_input("Enter your new First Name")
        
        changeb = st.button("Change First Name")
        if changeb:
            cur.execute('''
            UPDATE users_db
            SET first_name = %s
            WHERE id = %s
            ''', (changefname,st.session_state.user['first_name']))
            connection.commit()
            st.success("Updated Successfully")
    else:
        st.error("not selected")
    change_last_name = st.checkbox("Want to change your Last Name?")

    if change_last_name:
        changelname = st.text_input("Enter your new Last Name")
        changel = st.button("Change Last Name")
        if changel:
            cur.execute('''
            UPDATE users_db
            SET last_name = %s
            WHERE id = %s
            ''', (changelname,st.session_state.user['last_name']))
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
            ''', (changedob,st.session_state.user['dob']))
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
                    ''', (hashpass,st.session_state.user[0]))
                    connection.commit()
                    st.success("Password Updated Successfully")
    st.subheader("Upload Data File (Limit: 10MB per file)")
    #uploaded_file = st.file_uploader("Choose a CSV file (Max 10MB)", type="csv", accept_multiple_files=False)
    #upload_data(uploaded_file)
    datamgmt()
