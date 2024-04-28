'''
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd

app = FastAPI()

@app.post("/upload")
async def upload_data(file: UploadFile = File(...)):
    try:
        # Check if file is uploaded
        if file is None:
            return JSONResponse(status_code=400, content={"error": "Please upload a CSV file."})

        # Check file size
        if file.content_length > 10 * 1024 * 1024:  # 10MB limit
            return JSONResponse(status_code=400, content={"error": "File size exceeds the limit (10MB). Please upload a smaller file."})

        # Read uploaded file
        df = pd.read_csv(file.file)
        
        # Perform further processing and data upload
        # (Your code for processing and uploading data goes here)

        return JSONResponse(status_code=200, content={"message": "Data uploaded successfully!"})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Failed to upload data: {str(e)}"})

        '''
# backend.py

import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
from uuid import uuid4

app = FastAPI()

UPLOADS_BASE_DIR = "uploads/"

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Generate a unique filename for the uploaded file
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{str(uuid4())}.{file_extension}"
        file_path = os.path.join(UPLOADS_BASE_DIR, unique_filename)

        # Save the uploaded file to the specified directory
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Return a JSON response with the uploaded file information
        return JSONResponse({"message": "File uploaded successfully", "file_name": unique_filename})

    except Exception as e:
        return JSONResponse({"message": f"Failed to upload file: {str(e)}"}, status_code=500)
