import instaloader
import pandas as pd
from datetime import datetime,timedelta
# Initialize Instaloader object
def insta_scrapping(type):
    L = instaloader.Instaloader()
    L.save_metadata=False
    L.download_video_thumbnails = False
    L.save_caption=False
    L.download_videos=False
    try:
        L.load_session_from_file("sasashag")
    except FileNotFoundError:
        # If no session file exists, you need to log in interactively
        L.context.log("Session file does not exist. Logging in...")
        L.interactive_login("sasashag")
    if type=="male":
        data=pd.read_csv("Insta Scrapping\men.csv")
    else:
        data=pd.read_csv("Insta Scrapping\women.csv")
    data=data["Account"].tolist()
    current_date = datetime.now().date()
    filePath="instagram_"+type+"_"+current_date.strftime("%d-%m-%Y")
    j=0
    for i in data:
        try:
            j+=1
            profile = instaloader.Profile.from_username(L.context,i)
        except:
            continue
        print("\n",j,")",i)
        count=0
        for post in profile.get_posts():
            post_date=post.date_utc.date()
            try:
                if(count<=3):
                    print(count)
                    count=count+1
                    L.download_post(post,target=filePath)
                else:
                    break
            except:
                continue
    return filePath
print(insta_scrapping("women"))
