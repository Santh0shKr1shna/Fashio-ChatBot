from datetime import datetime,timedelta
from pinscrape import pinscrape
def download_pintrest(data,type):
    current_date = datetime.now().date()
    current_date.strftime("%d-%m-%Y")
    filePath="media\pinterest_"+current_date.strftime("%d-%m-%Y")+"\\"+type
    for i in data:
        print(i)
        details = pinscrape.scraper.scrape(i,filePath, {}, 10, 15)
        if details["isDownloaded"]:
            print("\nDownloading completed !!")
            print(f"\nTotal urls found: {len(details['extracted_urls'])}")
            print(f"\nTotal images downloaded (including duplicate images): {len(details['url_list'])}")
            print(details)
        else:
            print("\nNothing to download !!")
data_women=["Women T-Shirts","Women fashion","Women Clothes", "Women dress","cocktail dresses for women","Party dresses for women","Summer dresses for women","dresses for women","ladies dresses"]
data_men=["men T-Shirts","men fashion","men Clothes", "men dress","cocktail dresses for men","Party dresses for men","Summer dresses for men","dresses for men","men dresses"]
download_pintrest(data_men,"male")