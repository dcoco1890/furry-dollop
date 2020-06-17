import boto3
import os
import requests
from flask import redirect, render_template, request, session
from functools import wraps
# from PIL import Image

BUCKET = 'furrydollop'


# writing this for later to require login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/register")
        return f(*args, **kwargs)
    return decorated_function


def upload_file(file_name, bucket):
    # Set object name as name of file provided
    obj_name = file_name
    # Activate the boto3 client and tell it I'm using s3
    s3_client = boto3.client('s3')
    # Test to see stuff
    # x = s3_client.list_buckets()
    # print(x)
    # Variable res(ponse) is what is returned from the upload
    res = s3_client.upload_file(file_name, bucket, obj_name)
    print(res)
    return res
