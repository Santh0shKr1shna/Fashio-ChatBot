import requests
from bs4 import BeautifulSoup
import urllib.parse

# web scrapper
product = {"q": "men's puma running shoes"}
product_url = urllib.parse.urlencode(product)
url = f"https://www.flipkart.com/search?{product_url}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"

print(url)

r = requests.get(url)

soup = BeautifulSoup(r.content, 'html5lib')

with open("index.html", "w", encoding="utf-8") as file:
  file.write(r.text)

article_rows = soup.find('div', attrs={'class': '_1YokD2 _3Mn1Gg'})

articles = []

for item in article_rows.findAll('div', attrs={'class':'_1xHGtK _373qXS'}):
  if "Sponsored" in item.text:
    continue
  art = {}
  art['brand'] = item.find('div', attrs={'class': '_2WkVRV'}).text
  art['title'] = item.find('a', attrs={'class': 'IRpwTa'}).text
  art['link'] = "https://www.flipkart.com" + item.find('a', attrs={'class': 'IRpwTa'})["href"]
  art['price'] = int(item.find('div', attrs={'class': '_30jeq3'}).text.strip('₹').replace(',',''))
  art['image'] = item.find('img', attrs={'class': '_2r_T1I'})["src"]
  articles.append(art)
  
for a in articles:
  for k in a:
    print(k,":",a[k])
  print()

# print(soup.prettify())