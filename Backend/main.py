import json
import os
import requests

import matplotlib.pyplot as plt
import cv2
from PIL import Image

from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import subprocess
import base64
from io import BytesIO

# Local imports
import Langchain.db as db
import Langchain.Chat as Chat
import Langchain.Scrapper as scrapper
# from  import GoogleTrends

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
chat = Chat.Chat()
scrapper = scrapper.WebScrapper()

user = None
chatBot = None

def init_bot():
  if not user: return
  chatBot = chat.convo_with_summarize(database.load_convo())

@app.post('/login')
async def index(data: dict):
  uname= data.get('uname')
  pwd=data.get('pwd')
  if not uname and not pwd:
    raise HTTPException(status_code=400, detail="Empty data fields")
  
  try:
    check=database.login(uname, pwd)
    if(check):
      user = uname
      init_bot()
      return {"message": "Logged in successfully"}
    else:
      raise HTTPException(status_code=400, detail="Check details!")
  except:
    raise HTTPException(status_code=500, detail="Server error")

@app.post("/signup")
def index(data: dict):
  print(data)
  uname = data.get('name')
  pwd = data.get('pwd')
  if not uname and not pwd:
    raise HTTPException(status_code=400, detail="Empty data fields")
  
  #check if user already exists
  try:
    check = database.checkUser(uname)
    print(check)
    if check==2:
      raise HTTPException(status_code=400, detail="User already exists!")
  except:
    raise HTTPException(status_code=500, detail="Server Error")
  
  #if not signup
  try:
    check = database.signup(uname, pwd)
    if not check:
      raise HTTPException(status_code=400, detail="Check details!")
  except:
    raise HTTPException(status_code=500, detail="Server Error")
  
  details = {}
  details['name'] = data.get('name')
  details['age'] = data.get('age')
  details['gender'] = data.get('gender')
  details['region'] = data.get('address')
  details['likes'] = data.get('likes')
  details['dislikes'] = data.get('dislikes')
  details['favourite_colour'] = data.get('colors')
  details['favourite_dress'] = data.get('favourite_dress')
  
  try:
    summarized_text = chat.summarize(str(details), 50)
    res = database.save_convo(summarized_text)
    if not res:
      raise HTTPException(status_code=400, detail="Check details!")
  except Exception as e:
    print(e)
  
  user = uname
  init_bot()

@app.post("/trending")
def trending():
  try:
    gender = database.getGender()
    
  except Exception as e:
    print(e)

@app.get("/predict")
def predict(query: str):
  if not user or not chatBot:
    raise Exception("User not logged in or Chat bot not init")
  
  res = chatBot.predict(input=query)
  print("AI response: ", res)
  
  response = {"message": res}
  
  products = chat.extract_products(res)
  if len(products) < 2:
    return response
  
  response['products'] = []   # list format: [article_name, link, path_to_img]

  try:
    for product in products:
      scrapped_prods = scrapper.scrape(product, 1)
      art = []
      for i,item in enumerate(scrapped_prods):
        link = item.get('link')
        link_to_img = item.get('link_to_image')
        brand = item.get('brand').replace(' ','')

        art.append(item.get('title'))
        art.append(link)
        
        img = requests.get(link_to_img)
        if img.status_code:
          img_path = f"../images/{brand}_{i}"
          fp = open(img_path, 'wb')
          fp.write(img.content)
          fp.close()
          art.append(img_path)
          
      response['products'].append(art)
  
  except Exception as e:
    raise e
  
  return response


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

@app.post("/close")
def close():
  summary = chatBot.memory.moving_summary_buffer
  
  try:
    database.save_convo(summary)
  except Exception as e:
    print(e)
  
  # user = None
  # chatBot = None