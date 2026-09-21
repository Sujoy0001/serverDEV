import os
from fastapi import FastAPI, File, UploadFile, HTTPException, status
import boto3
from .config import AWS_REGION, AWS_ACCESS_KEY_ID, AWS_ENDPOINT_URL_S3, AWS_SECRET_ACCESS_KEY

app = FastAPI()



s3 = boto3.client(
    "s3",
    aws_endpoint_url
    region_name=AWS_REGION)
bucket = "avaters"

@app.get("/")
def root():
    return {"message" : "Server is running..."}

@app.post("/uploadfile/", status_code=status.HTTP_200_OK)
async def create_upload_file(file: UploadFile):
    key = f"SUJOY - {file.filename}"
    
    try:
        s3.put_object(Bucket=bucket, Key=key, Body=file)
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Storage upload failed: {str(e)}")
    
    return {"message" : file.filename}