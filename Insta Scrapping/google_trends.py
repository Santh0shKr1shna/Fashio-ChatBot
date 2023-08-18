from pytrends.request import TrendReq
from datetime import datetime,timedelta
def google_trends(data,type,country,region):
    current_date = datetime.now().date()
    previous_date=current_date-timedelta(days=1)
    current_date=current_date.strftime("%Y-%m-%d")
    previous_date=previous_date.strftime("%Y-%m-%d")
    # tf=previous_date+" "+current_date
    # print(tf)
    region_based_search={}
    location=country+"-"+region
    pytrends = TrendReq(hl='en-US', tz=360,geo=location)
    for i in data:
        pytrends.build_payload(kw_list=[i])
        values=pytrends.related_queries()[i]["rising"]
        if(values is None):
            region_based_search[i]=""
        else:
            region_based_search[i]=values["query"].to_list()[0:5]
    return region_based_search






data_women=["Women T-Shirts","Women fashion","Women Clothes", "Women dress","cocktail dresses for women","Party dresses for women","Summer dresses for women","dresses for women","ladies dresses"]
data_men=["men T-Shirts","men fashion","men Clothes", "men dress","cocktail dresses for men","Party dresses for men","Summer dresses for men","dresses for men","men dresses"]
dict=google_trends(data_men,"men","IN","TN")
for i in dict:
    print(i,":",dict[i])