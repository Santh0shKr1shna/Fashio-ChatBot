import json

import matplotlib.pyplot as plt
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
import cv2
import subprocess
import os
from pydantic import BaseModel
import base64
import Langchain.db as db
from io import BytesIO
from PIL import Image

#paths
VTON_IMG_UPLOAD_DIR = "./Virtual_TON"

#FastAPI
app=FastAPI()

#image holders
class ImageData(BaseModel):
    image1: str
    image2: str
    
class SurveyData(BaseModel):
    name: str
    age: int
    email: str
    gender: str
    address: str
    likes: list[str]
    dislikes: list[str]
    colors: str
    favourite_dress: str
    pwd: str
    
    def __getitem__(self, item):
        if item == 'name': return self.name
        elif item == 'age': return self.age
        elif item == 'gender':return self.gender
        elif item == 'region': return self.address
        elif item == 'likes': return self.likes
        elif item == 'dislikes': return self.dislikes
        elif item == 'colors': return self.colors
        elif item == 'favourite_dress': return self.favourite_dress
        else:
            raise "No such member found"


database = db.DataBase()
user = None

@app.post('/login')
def index(uname, pwd):
    if not uname and not pwd:
        raise HTTPException(status_code=400, detail="Empty data fields")

    try:
        check=database.login(uname, pwd)
        if(check):
            return {"message": "Logged in successfully"}
        else:
            raise HTTPException(status_code=400, detail="Check details!")
    except:
        raise HTTPException(status_code=500, detail="Server error")

@app.post("/signup")
def index(data: SurveyData):
    uname = data.name
    pwd = data.pwd
    if not uname and not pwd:
        raise HTTPException(status_code=400, detail="Empty data fields")
    
    try:
        check = database.signup(uname, pwd)
        if not check:
            raise HTTPException(status_code=400, detail="Check details!")
    except:
        raise HTTPException(status_code=500, detail="Server Error")
    
    details = {}
    details['name'] = data.name
    details['age'] = data.age
    details['gender'] = data.gender
    details['region'] = data.address
    details['likes'] = data.likes
    details['dislikes'] = data.dislikes
    details['favourite_colour'] = data.colors
    details['favourite_dress'] = data.favourite_dress
    
    try:
        res = database.save_convo(str(details))
        if not res:
            raise HTTPException(status_code=400, detail="Check details!")
    except:
        raise HTTPException(status_code=500, detail="Server error")
    

@app.get("/chat")
def predict(query: str):
    return 0

@app.post("/vton/")
def generate(data: ImageData, request: Request):

    # Decode base64 strings to bytes
    image1_bytes = base64.b64decode(data.image1)
    image2_bytes = base64.b64decode(data.image2)
    
    # Open images using PIL
    image1 = Image.open(BytesIO(image1_bytes))
    image2 = Image.open(BytesIO(image2_bytes))

    # Save images to a specified location
    image1_path = os.path.join(f"{VTON_IMG_UPLOAD_DIR}/static/", "origin_web.jpg") #person_image
    image2_path = os.path.join(f"{VTON_IMG_UPLOAD_DIR}/static/", "cloth_web.jpg")

    with open(image1_path, "wb") as f:
        f.write(image1_bytes)

    with open(image2_path, "wb") as f:
        f.write(image2_bytes)

    #run the model and generate the output
    dmc=f"python {VTON_IMG_UPLOAD_DIR}/main.py --background false"
    try:
        subprocess.run(dmc,shell=True)
    except subprocess.CalledProcessError:
        print ('Error in Main function')

    with open(f"{VTON_IMG_UPLOAD_DIR}/static/finalimg.png", "rb") as f:
        finalImg = base64.b64encode(f.read()).decode("utf-8")
    
    return {"image": finalImg}