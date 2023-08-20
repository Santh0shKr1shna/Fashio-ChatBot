from db import DataBase
from Chat import Chat


class Bot(object):
  db = DataBase()
  chat = Chat()
  user = None
  conversation = None
  
  def __init__(self):
    uname = ''
    if self.db.login():
      self.user = uname
  
  def predict(self, query) -> str:
    if not self.user:
      return ''
  
  def signup(self):
    pass
  
  """
   Fields required:
   -> Name
   -> Age
   -> Region
   -> Likes and dislikes
   -> Fav colour
   -> Favourite fashion attires
   -> Scrape wishlist
  """
  
  def get_user_details(self) -> str:
    return str(
      {
        'name': 'santhosh',
        'age': 20,
        'region': 'India',
        'likes and dislikes': 'subtle fashion, light themed clothes, cool outfits with minimal accessories',
        'favourite colour': 'cream, beige, blue',
        'favourite fashion attire': 'sweatshirts and cotton pants'
      }
    )
  
  def sign_up_summarizer(self):
    self.db.login()
    
    details = self.get_user_details()
    print("LOG::Details text: ", details)
    
    summarized_text = self.chat.summarize(details, 50)
    print("LOG::Summarized text: ", summarized_text)
    
    self.db.save_convo(summarized_text)


if __name__ == '__main__':
  pass
  # bot = Bot()
  #
  # chars = bot.db.load_convo()
  # print(chars)
  # conversation = bot.chat.KGmemory(chars)
  #
  # done = True
  # while done:
  #   res = conversation.predict(input=input("Enter prompt: "))
  #   print(res)
  #   if input("Want to continue(Y/N): ") == 'N':
  #     done = False