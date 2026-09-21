import os
import boto3

s3 = boto3.client("s3", region_name=os.environ["AWS_REGION"])
bucket = "assets"
key = "uploads/file.txt"

s3.put_object(Bucket=bucket, Key=key, Body="Hello World!")

url = s3.generate_presigned_url("get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=3600)
print(f"[view] {url}")

