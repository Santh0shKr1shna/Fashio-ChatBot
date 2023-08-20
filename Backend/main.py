import matplotlib.pyplot as plt
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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


# Configure CORS settings
origins = [
    "http://localhost:3000",  # Replace with your React app's URL
    "https://your-react-app-domain.com"  # Add more origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
#image holders
class ImageData(BaseModel):
    image1: str
    image2: str


@app.post('/login')
async def index(data: dict):
    uname= data.get('uname')
    pwd=data.get('pwd')
    if not uname and not pwd:
        raise HTTPException(status_code=400, detail="Empty data fields")
    database=db.DataBase()
    try:
        check=database.login(uname, pwd)
        if(check):
            return {"message": "Logged in successfully"}
        else:
            raise HTTPException(status_code=400, detail="Check details!")
    except:
        raise HTTPException(status_code=500, detail="Server error")

@app.get("/")
def index():
    return {"message": "hola"}

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
