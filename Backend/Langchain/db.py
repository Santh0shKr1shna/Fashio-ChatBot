import sqlite3


class DataBase(object):
  user = None
  con, cur = None, None
  
  def __init__(self):
    db_path = "C:\sqlite\chatbot.db"
    self.con = sqlite3.connect(db_path, check_same_thread=False)
    print("LOG: Database connected")
    self.cur = self.con.cursor()
    print("LOG: Cursor set")
    
  def login(self, uname, pwd) -> int:
      res = None
      try:
        self.cur.execute(f"SELECT pwd FROM users WHERE username = '{uname}'")
        res = self.cur.fetchone()
      
      except sqlite3.Error as error:
        print("Error: ", error)
        return 0
      
      if not res:
        print("Username does not exist! Please sign up")
        return 0
      
      if pwd.strip() != res[0]:
        print("Password does not match! Retry")
        return 0
      
      self.user = uname
      print("User signed in")
      return 1
  
  def checkUser(self, uname):
    try:
      self.cur.execute(f"SELECT * FROM users where username='{uname}';")
      res=self.cur.fetchone()
      if res:
        print("User already exists!")
        return 2
    except sqlite3.Error as e:
      print("Error while checking user: ", e)
      return 0
    return 1

  def signup(self, uname, pwd) -> int:
    try:
      self.cur.execute(f"INSERT INTO users VALUES('{uname}', '{pwd}');")
      self.con.commit()
      
      self.cur.execute(f"INSERT INTO prev_convos VALUES('{uname}', '');")
      self.con.commit()
    
    except sqlite3.Error as e:
      print("LOG:: Error while signup: ", e)
      return 0
    
    self.user = uname
    return 1
  
  def load_convo(self) -> str:
    if not self.user:
      return ""
    
    res = None
    try:
      self.cur.execute(f"SELECT convo_summary FROM prev_convos WHERE username = '{self.user}'")
      res = self.cur.fetchone()
    except sqlite3.Error as e:
      print("LOG::Loading error: ", e)
    
    if not res:
      print("LOG::No records found from load_convo")
      return ""
    
    return res[0]
  
  def save_convo(self, new_convo) -> int:
    if not self.user:
      return 0
    
    try:
      print("Hola")
      self.cur.execute(f"UPDATE prev_convos SET convo_summary = '{new_convo}' WHERE username = '{self.user}'")
      self.con.commit()
      print("LOG::Data updated in prev_convos")
    
    except sqlite3.Error as e:
      print("LOG::Error saving data: ", e)
      return 0
    
    return 1


if __name__ == "__main__":
  pass
  # db = DataBase()
  # db.login()
  # print(db.save_convo('new test save'))