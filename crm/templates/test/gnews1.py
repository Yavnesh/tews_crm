from gnews import GNews
import requests, json
import pandas as pd
from pytrends.request import TrendReq
from pytrends.request import TrendReq
import newspaper
from newspaper import Config, Article, Source

########################################## GNews Function Starts #####################################################
pytrends = TrendReq(hl='en-US', tz=360)
trending_list = pytrends.realtime_trending_searches(pn='US')['entityNames'].tolist()
items = []
count = 0
for item in trending_list:
    items.append(item)
    count = count + 1
    # for t in item:
print("items",items)
print("items hgf ",items[0])
result = " ".join(items[10])
print("count",count)
google_news = GNews()
json_resp = google_news.get_news(result)
i=0
items = 0
title = []
text = []
images = []
url = []

config = Config()
config.request_timeout = 20
jsonrep_resp = json.dumps(json_resp)
json_resp = json.loads(jsonrep_resp)
for item in json_resp:
    i = i+1        
    url_path = item['url']
    article = newspaper.Article(url=item['url'], config=config)
    try:
        article.download()
        try:
            article.parse()
            img = []
            print("check")
            for item in article.images:
                img.append(str(item))
            title.append(article.title)
            text.append(article.text)
            images.append(img)
            url.append(url_path)
            
            items = items + 1
            if items == 10:
                print("break")
                break

        except Exception as e:
            print(e)
    except Exception as e:
        print(e)

title = json.dumps(title)
content = json.dumps(text)
images = json.dumps(images)
url = json.dumps(url)
print(title)

########################################## GNews Function End #####################################################
