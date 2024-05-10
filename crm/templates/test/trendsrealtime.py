
from pytrends.request import TrendReq
import time
# related_topics = {
#     'Tornado': {
#         'rising': {
#             'value': [],
#             'topic_title': []
#         },
#         'top': {
#             'value': [100, 16, 4, 3, 2, 1, 1, 1],
#             'topic_title': ['Tornado', 'Tornado warning', 'Radar', '2013 Moore Tornado', 'Severe thunderstorm warning', 'Siren', 'Civil defense siren', 'Joplin']
#         }
#     }
# }
# related_topics = {
#     'Tornado': {
#         'rising': {
#             'value': [850, 200, 190, 150],
#             'topic_title': ['Severe thunderstorm warning', 'Radar', '2013 Moore Tornado', 'Tornado warning']
#         },
#         'top': {
#             'value': [100, 16, 4, 3, 2, 1, 1, 1],
#             'topic_title': ['Tornado', 'Tornado warning', 'Radar', '2013 Moore Tornado', 'Severe thunderstorm warning', 'Siren', 'Civil defense siren', 'Joplin']
#         }
#     }
# }
def extract_topic_titles(related_topics,t):
    topic_titles_rising = []
    topic_titles_top = []
    try:
        # Check if 'rising' key exists and has data
        if 'rising' in related_topics[t] and not related_topics[t]['rising'].empty:
            topic_titles_rising.extend(related_topics[t]['rising']['topic_title'])

        # Check if 'top' key exists and has data
        if 'top' in related_topics[t] and not related_topics[t]['top'].empty:
            topic_titles_top.extend(related_topics[t]['top']['topic_title'])

    except KeyError:
        print("No data available for related topics.")

    return topic_titles_rising, topic_titles_top


pytrends = TrendReq()
TrendingList = pytrends.realtime_trending_searches(pn='US')
trending_list = TrendingList['entityNames'].tolist()

timeframe=['now 1-d']
geo='US'
for item in trending_list:
    print("item", item)
    for t in item:
        pytrends.build_payload([t], cat = 0, timeframe = timeframe, geo = geo, gprop = '')

        related_topics = pytrends.related_topics()
        
        related_query = pytrends.related_queries()

        topic_titles_rising, topic_titles_top = extract_topic_titles(related_topics,t)
        print("Extracted topic titles:", topic_titles_rising)

        print("Extracted topic titles:", topic_titles_top)
    time.sleep(5)
