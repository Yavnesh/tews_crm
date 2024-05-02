from gnews import GNews
import requests
import pandas as pd
from pytrends.request import TrendReq

import newspaper
from newspaper import Config, Article, Source
# # connect to google


########################################## Pytrends Function Starts #####################################################


# pytrends = TrendReq(hl='en-US', tz=360)
# print(pd.__version__)
# TrendingList = pytrends.trending_searches(pn='united_states')
# # print(type("TrendingList"))

# trending_list = TrendingList.values.tolist()
# # print(trending_list)
# flat_list = [item for sublist in trending_list for item in sublist]
# print(flat_list)


# for item in flat_list:
#     pytrends.build_payload([item], cat=0, timeframe='today 5-y', geo='US', gprop='')

#     related_topics = pytrends.related_topics()
#     if item in related_topics and 'rising' in related_topics[item] and 'topic_title' in related_topics[item]['rising']:
#         t_rising = related_topics[item]['rising']['topic_title']
#         related_topics_rising = t_rising.values.tolist()
#         print(related_topics_rising)


########################################## Pytrends Function Ends #####################################################



########################################## GNews Function Starts #####################################################

google_news = GNews()
json_resp = google_news.get_news("Japanese yen dollar")
i=0
items = 0
title = []
text = []
images = []
url = []

config = Config()
config.request_timeout = 20

for item in json_resp:
    i=i+1
    print("i--",i)
    
    article = newspaper.Article(url=item['url'], config=config)
    try:
        article.download()
        print("Article downloaded successfully!")
        try:
            article.parse()
            print("Article Parsed successfully!")

            title.append(article.title)
            text.append(article.text)
            images.append(article.images)
            
            print("items--",items, "--title--",article.title)
            # print("items--",items, "--text--",article.text)
            # print("items--",items, "--images--",article.images)
            print("items--",items, "--url--",item['url'])

            items = items + 1
            if items == 10:
                print("break")
                break

        except Exception as e:
            print("Article Not Parsed !")

    except Exception as e:
        print("Article Not Downloaded")

print("title",title)
# print("text",text)
# print("images",images)
print("url",url)


########################################## GNews Function End #####################################################




# # realtime search trends for United States, India
# realTimeTrendUS = pytrends.realtime_trending_searches(pn='US') 
# print(realTimeTrendUS)
# print(realTimeTrendUS[0].tolist())






# print(usTrending.keys())
# all_values_list = [[row[col] for col in usTrending.columns] for idx, row in usTrending.iterrows()]
# values_list = [item[0] for sublist in all_values_list]
# print(values_list)
# print("all_values_list",all_values_list)  # Output: [[1, 'a'], [2, 'b'], [3, 'c']]
# # Extract values from all columns
# column_values_list = usTrending.tolist(axis=1)
# print(column_values_list)  # Output: [[1, 2, 3], ['a', 'b', 'c']]

# # Extract values from a specific column
# col1_values_list = usTrending['col2'].to_list()
# print(col1_values_list)  # Output: [1, 2, 3]
# # basic request // single keyword
# kw_list = ["recession"]
# # five keyword max per request
# # kw_list = ["crypto", 
# #             "bitcoin", 
# #             "ethereum", 
# #             "AI", 
# #             "Tesla"
# #           ]

# # last five years of data
# # pytrends.build_payload(kw_list, 
# #                        cat=0, 
# #                        timeframe='today 5-y', 
# #                        geo='', 
# #                        gprop=''
# #                       )

# # last year of data
# pytrends.build_payload(kw_list, 
#                         cat=0, 
#                         timeframe='today 12-m', 
#                         geo='', 
#                         gprop=''
#                       )

# # specific range of daily data
# # pytrends.build_payload(kw_list, 
# #                         cat=0, 
# #                         timeframe='2016-12-14 2017-01-25', 
# #                         geo='', 
# #                         gprop=''
# #                       )

# # NO multirange or historical hourly interest functions 

# # minute data last 4 hours
# # pytrends.build_payload(kw_list, 
# #                         cat=0, 
# #                         timeframe='now 4-H', 
# #                         geo='', 
# #                         gprop=''
# #                       )

# # hour data last 7 days
# # pytrends.build_payload(kw_list, 
# #                         cat=0, 
# #                         timeframe='now 7-d', 
# #                         geo='', 
# #                         gprop=''
# #                       )

# # hour data last 7 days starting 7 days ago
# # pytrends.build_payload(kw_list, 
# #                         cat=0, 
# #                         timeframe='2023-02-03T10 2023-02-10T10', 
# #                         geo='', 
# #                         gprop=''
# #                       )

# # # interest over time
# # iot = pytrends.interest_over_time()
# # iot.plot()

# # # regional data // resolution=['CITY','COUNTRY','REGION','DMA'][1]
# # regionData = pytrends.interest_by_region(resolution='COUNTRY', 
# #                                           inc_low_vol=True, 
# #                                           inc_geo_code=False
# #                                         )

# # # related topics, queries use with single keyword only
# # relatedTopics = pytrends.related_topics()
# # relatedTopics.keys()
# # relatedTopics[kw_list[0]]
# # relatedTopics[kw_list[0]]['rising']
# # relatedTopics[kw_list[0]]['rising'].columns
# # relatedTopics[kw_list[0]]['rising']['topic_title']
# # relatedTopics[kw_list[0]]['top']
# # relatedTopics[kw_list[0]]['top'].columns
# # relatedTopics[kw_list[0]]['top']['topic_title']

# # relatedQueries = pytrends.related_queries()
# # relatedQueries.keys()
# # relatedQueries[kw_list[0]]
# # relatedQueries[kw_list[0]].keys()
# # relatedQueries[kw_list[0]]['rising']
# # relatedQueries[kw_list[0]]['rising']['query']
# # relatedQueries[kw_list[0]]['top']
# # relatedQueries[kw_list[0]]['top'].columns
# # relatedQueries[kw_list[0]]['top']['query']

# # trending searches
# usTrending = pytrends.trending_searches(pn='united_states')
# print(usTrending)
# # japanTrending = pytrends.trending_searches(pn='japan')

# # # realtime search trends for United States, India
# # realTimeTrendUS = pytrends.realtime_trending_searches(pn='US') 
# # realTimeTrendIN = pytrends.realtime_trending_searches(pn='IN')

# # # top charts // global
# # yearDate = 2022
# # topCharts = pytrends.top_charts(yearDate, hl='en-US', tz=300, geo='GLOBAL')

# # # keyword suggestions // use with CAUTION
# # suggestions = pytrends.suggestions(kw_list[0])

# # # get all categories
# # cats = pytrends.categories()
# # cats.keys()
# # cats['name']
# # cats['children']
# # cats['children'][0]
# # cats['children'][0]['name']
# # cats['children'][0]['children']
# # cats['children'][0]['children'][0]
# # cats['children'][0]['children'][0]['id']


