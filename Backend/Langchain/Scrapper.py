import requests
from bs4 import BeautifulSoup
import urllib.parse

# web scrapper

class WebScrapper(object):
  articles = []
  
  def scrape(self, query, no_of_items):
    product = {"q": query}
    product_url = urllib.parse.urlencode(product)

    url = f"https://www.flipkart.com/search?{product_url}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    
    r = requests.get(url)
    self.save_page(r)
    
    soup = BeautifulSoup(r.content, 'html5lib')

    article_rows = soup.find('div', attrs={'class': '_1YokD2 _3Mn1Gg'})
    self.articles = []

    for item in article_rows.findAll('div', attrs={'class': '_1xHGtK _373qXS'}):
      if "Sponsored" in item.text:
        continue
      art = {}
      art['brand'] = item.find('div', attrs={'class': '_2WkVRV'}).text
      art['title'] = item.find('a', attrs={'class': 'IRpwTa'}).text
      art['link'] = "https://www.flipkart.com" + item.find('a', attrs={'class': 'IRpwTa'})["href"]
      art['price'] = int(item.find('div', attrs={'class': '_30jeq3'}).text.strip('₹').replace(',', ''))
      art['link_to_image'] = item.find('img', attrs={'class': '_2r_T1I'})["src"]
      self.articles.append(art)
      
    return self.articles[:no_of_items] if no_of_items < len(self.articles) else self.articles
  
  def scrape_wishlist (self):
    url = "https://www.flipkart.com/wishlist?link=home_wishlist"
    
    r = requests.get(url)
    
    soup = BeautifulSoup(r.content, 'html5lib')

    article_rows = soup.find('div', attrs={'class': '_3E8aIl sTQ7AV'})
    wishlist = []
    
    for item in article_rows.findAll('div', attrs={'class': '_1M-Ete'}):
      art = {}
      art['brand'] = item.find('div', attrs={'class': '_2WkVRV'}).text
      art['title'] = item.find('div', attrs={'class': '_3hscEA'}).text
      art['link'] = "https://www.flipkart.com" + item.find('a', attrs={'class': 'IRpwTa'})["href"]
      art['price'] = int(item.find('div', attrs={'class': '_30jeq3'}).text.strip('₹').replace(',', ''))
      art['link_to_image'] = item.find('img', attrs={'class': '_396cs4'})["src"]
      wishlist.append(art)



  def save_page(self, r):
    with open("index.html", "w", encoding="utf-8") as file:
      file.write(r.text)

  def print_articles(self):
    for a in self.articles:
      for k in a:
        print(k,":",a[k])
      print()
