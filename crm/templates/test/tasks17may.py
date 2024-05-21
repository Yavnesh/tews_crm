import os, json,requests
from crm.models import Scrape, Post, TwitterPost, Trending
from crm.fun_gemini import generate_image_prompt, generate_content_info, generate_content, split_text, generate_content_cta,generate_meta_info, generate_short_content, generate_trend_topics
from crm.fun_horde import generate_image_api

##############  Celery  #######################
from celery import shared_task
from django_celery_beat.models import PeriodicTask, IntervalSchedule

##############  Tweepy  #######################
import tweepy

##############  Gemini  #######################
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

##############  Horde  #######################
import asyncio

##############  GNews  #######################
from gnews import GNews

##############  PyTrends  #######################
from pytrends.request import TrendReq

##############  Newspaper  #######################
import newspaper
from newspaper import Config

##############  Loguru  #######################
from loguru import logger
logger.add("logs/file_{time}.log",level="TRACE", rotation="10 MB")
# logger.add("logs/testing.log",level="TRACE", rotation="10 MB")
########################### Gemini Tasks ######################################################
#Create scrape_url Task every 1 min
schedule60, created60 = IntervalSchedule.objects.get_or_create(every=60, period=IntervalSchedule.SECONDS )
schedule30, created30 = IntervalSchedule.objects.get_or_create(every=30, period=IntervalSchedule.SECONDS )

#Schedule the periodic task programmatically

PeriodicTask.objects.get_or_create(
    interval = schedule30,
    name = 'generate_short_content_task_periodic',
    task = 'crm.tasks.generate_short_content_task',
)

PeriodicTask.objects.get_or_create(
    interval = schedule30,
    name = 'generate_realated_trend_task_periodic',
    task = 'crm.tasks.generate_realated_trend_task',
)

PeriodicTask.objects.get_or_create(
    interval = schedule30,
    name = 'generate_content_info_task_periodic',
    task = 'crm.tasks.generate_content_info_task',
)

PeriodicTask.objects.get_or_create(
    interval = schedule60,
    name = 'generate_content_task_periodic',
    task = 'crm.tasks.generate_content_task',
)

PeriodicTask.objects.get_or_create(
    interval = schedule30,
    name = 'generate_meta_info_task_periodic',
    task = 'crm.tasks.generate_meta_info_task',
)

PeriodicTask.objects.get_or_create(
    interval = schedule30,
    name = 'generate_image_prompt_task_periodic',
    task = 'crm.tasks.generate_image_prompt_task',
)

# PeriodicTask.objects.get_or_create(
#     interval = schedule60,
#     name = 'generate_twitter_post_task_periodic',
#     task = 'crm.tasks.generate_twitter_post_task',
# )

PeriodicTask.objects.get_or_create(
    interval = schedule60,
    name = 'fetch_api_website_task_periodic',
    task = 'crm.tasks.fetch_api_website',
)

# ########################### Twitter Tasks ######################################################

# PeriodicTask.objects.get_or_create(
#     interval = schedule60,
#     name = 'publish_twitter_post_task_periodic',
#     task = 'crm.tasks.publish_twitter_post_task',
# )

# ########################### Horde Tasks ######################################################

# # #Create scrape_url Task every 10 min
schedule90, created90 = IntervalSchedule.objects.get_or_create(every=90, period=IntervalSchedule.SECONDS )

PeriodicTask.objects.get_or_create(
    interval = schedule90,
    name = 'generate_image_task_periodic',
    task = 'crm.tasks.generate_image_task',
)

########################### PyTrend Tasks ######################################################
# # #Create scrape_url Task every 30 min
schedule1800, created1800 = IntervalSchedule.objects.get_or_create(every=1800, period=IntervalSchedule.SECONDS )
schedule900, created900 = IntervalSchedule.objects.get_or_create(every=900, period=IntervalSchedule.SECONDS )


PeriodicTask.objects.get_or_create(
    interval = schedule1800,
    name = 'fetch_trends_task_periodic',
    task = 'crm.tasks.fetch_trends_task',
)

PeriodicTask.objects.get_or_create(
    interval = schedule900,
    name = 'fetch_trends_realtime_task_periodic',
    task = 'crm.tasks.fetch_trends_realtime_task',
)

########################### GNews Tasks ######################################################
schedule120, created120 = IntervalSchedule.objects.get_or_create(every=120, period=IntervalSchedule.SECONDS )
PeriodicTask.objects.get_or_create(
    interval = schedule90,
    name = 'fetch_article_data_task_periodic',
    task = 'crm.tasks.fetch_article_data_task',
)


################################## Gemini Settings ####################################
# genai.configure(api_key="AIzaSyBJaCAFmsYpMcO7OTNEJV6I-Ci9O7-X03Q")
genai.configure(api_key="AIzaSyAZLlvQ2yyZxQ6WqfZ0uTBKIhVxU0c-Ml8")
model = genai.GenerativeModel('gemini-pro')

safety_setting={
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

################################## Task Functions ####################################


@logger.catch
@shared_task
def fetch_trends_task():
    logger.warning("Fetch Trends Task Started")

    try:
        # connect to google
        pytrends = TrendReq(hl='en-US', tz=360) #, timeout=(10,25), proxies=['https://181.143.106.162:52151', 'https://198.168.189.54:80', 'https://112.78.170.250:8080', 'https://186.96.50.113:999', 'https://148.244.210.141:999', 'https://146.190.101.222:3128', 'https://45.188.164.3:999', 'https://31.43.158.108:8888', 'https://187.251.102.50:999', 'https://117.54.114.102:80', 'https://124.106.150.231:8282', 'https://81.163.56.104:23500',], retries=2, backoff_factor=0.1, requests_args={'verify':False})
        logger.warning("Connected pytrends")
        
        TrendingList = pytrends.trending_searches(pn='united_states')
        trending_list = TrendingList.values.tolist()
        logger.warning("View Trending List",trending_list)
        
        topic_list = [item for sublist in trending_list for item in sublist]
        # i = 0
        for item in topic_list:
            logger.warning("For Loop Topic List")
            if not Trending.objects.filter(topic = item).exists():
                # i = i + 1
                # pytrends.build_payload([item], cat=0, timeframe='today 5-y', geo='US', gprop='')

                # related_topics = pytrends.related_topics()
                # related_query = pytrends.related_queries()

                # related_topics_rising, related_topics_top = get_related_topic(related_topics,item)
                # related_queries_rising, related_queries_top = get_related_query(related_query,item)
                related_topics_rising = []
                related_topics_top = []
                related_queries_rising = []
                related_queries_top = []

                trending_object = Trending(topic = item,
                                        related_topics_rising = json.dumps(related_topics_rising),
                                        related_topics_top = json.dumps(related_topics_top),
                                        related_query_rising = json.dumps(related_queries_rising),
                                        related_query_top = json.dumps(related_queries_top),
                                        source = "Daily Trends", status = "Saved")
                trending_object.save()
                logger.warning(f'Table Saved for topic {item}')
                # if i > 2:
                #     logger.warning(f'For Loop Topic List Count - {i}')
                #     break
        logger.warning("Fetch Trends Task Ended")
        return None

    except Exception as e:
        logger.warning(f'Fetch Trends Try Block Exception - {e}')
        return None

@logger.catch
@shared_task
def fetch_trends_realtime_task():
    logger.warning("Fetch Trends Real Time Task Started")
    try:
        # connect to google
        pytrends = TrendReq(hl='en-US', tz=360) #, timeout=(10,25), proxies=['https://181.143.106.162:52151', 'https://198.168.189.54:80', 'https://112.78.170.250:8080', 'https://186.96.50.113:999', 'https://148.244.210.141:999', 'https://146.190.101.222:3128', 'https://45.188.164.3:999', 'https://31.43.158.108:8888', 'https://187.251.102.50:999', 'https://117.54.114.102:80', 'https://124.106.150.231:8282', 'https://81.163.56.104:23500',], retries=2, backoff_factor=0.1, requests_args={'verify':False})
        logger.warning("Connected pytrends")
        


        TrendingList = pytrends.realtime_trending_searches(pn='US')
        topic_list = TrendingList['entityNames'].tolist()
        logger.warning("View Trending List",topic_list)
        
        # i = 0
        for item in topic_list:
            logger.warning("For Loop Topic List")
            for t in item:
                logger.warning("For Loop Topic List > Item")
                if not Trending.objects.filter(topic = t).exists():
                    # i = i+1
                    # pytrends.build_payload([t], cat=0, timeframe='now 1-d', geo='US', gprop='')

                    # related_topics = pytrends.related_topics()
                    # related_query = pytrends.related_queries()

                    # related_topics_rising, related_topics_top = get_related_topic(related_topics,t)
                    # related_queries_rising, related_queries_top = get_related_query(related_query,t)
                    related_topics_rising = []
                    related_topics_top = []
                    related_queries_rising = []
                    related_queries_top = []
                    trending_object = Trending(topic = t,
                                            related_topics_rising = json.dumps(related_topics_rising),
                                            related_topics_top = json.dumps(related_topics_top),
                                            related_query_rising = json.dumps(related_queries_rising),
                                            related_query_top = json.dumps(related_queries_top),
                                            source = "Real Time Trends", status = "Saved")
                    trending_object.save()
                    logger.warning(f'Table Saved for topic {t}')
            # if i > 3:
            #     logger.warning(f'For Loop Topic List Count {i}')
            #     break
        logger.warning("Fetch Trends Real Time Task Ended")
        return None

    except Exception as e:
        logger.warning(f'Fetch Trends Try Block Exception - {e}')
        return None

@logger.catch
@shared_task
def fetch_article_data_task():
    logger.warning("Fetch Article Data Task Started")
    try:
        if Trending.objects.filter(status = "Saved").exists():
            trending_object = Trending.objects.filter(status = "Saved").order_by('id').first()
            logger.warning(f'Get first item of Trending with status Saved,trending_object')
            if Scrape.objects.filter(trending_id = trending_object.id).exists():
                logger.warning("Trending item already exists")
            else:
                google_news = GNews()
                json_resp = google_news.get_news(trending_object.topic)
                chr_count = 0
                items = 0
                title = []
                text = []
                images = []
                url = []
                
                config = Config()
                config.request_timeout = 20
                for item in json_resp:
                    logger.warning("For loop in Gnews")
                    url_path = item['url']
                    article = newspaper.Article(url=item['url'], config=config)
                    try:
                        logger.warning("Article Download Starts")
                        article.download()
                        logger.warning("Article Download Successful")
                        try:
                            article.parse()
                            logger.warning("Article parse Successful")
                            img = []
                            for item in article.images:
                                img.append(str(item))
                            chr_count = chr_count + len(article.text)
                            if chr_count>50000:
                                logger.warning(f'For loop status break {chr_count}')
                                break
                            print("titarticle.titlele", article.title)
                            print("contenarticle.textt", article.text)
                            print("imagimges", img)
                            print("uurl_pathrl", url_path)
                            print()
                            title.append(article.title)
                            text.append(article.text)
                            images.append(img)
                            url.append(url_path)
                            
                            items = items + 1
                            if items == 10:
                                logger.warning(f'For loop status break {items}')
                                break
                            
                        except Exception as e:
                            logger.warning(f'Article Parse exception {e}')
                    except Exception as e:
                        logger.warning(f'Article Download exception {e}')

                title = json.dumps(title)
                content = json.dumps(text)
                images = json.dumps(images)
                url = json.dumps(url)
                print("title", title)
                print("content", content)
                print("images", images)
                print("url", url)

                if title and content and url:
                    logger.warning("Scrape Table items not empty")
                    if Scrape.objects.filter(trending_id = trending_object.id).exists():
                        logger.warning("Scrape Item already exists")
                    else:
                        if chr_count>10000:
                            scrape_object = Scrape( trending_id = trending_object.id,
                                                title = title,
                                                content = content,
                                                images = images,
                                                url = url,
                                                status = "Scraped")
                            scrape_object.save()
                            logger.warning("Scrape Table Saved")
                            trending_object.status = "Scraped"
                            trending_object.save()
                            logger.warning("Trending table Status updated")
                        else:
                            trending_object.status = "Blocked"
                            trending_object.save()
        logger.warning("Fetch Article Data Task Completed")
        return None

    except Exception as e:
        logger.warning(f'Fetch Article Data exception {e}')
        return None



@logger.catch
@shared_task
def generate_short_content_task():
    logger.warning("Generate Short Content Task Started")
    try:
        if Scrape.objects.filter(status="Scraped"):
            scrape_object = Scrape.objects.filter(status="Scraped").order_by('id').first()
            print(scrape_object.trending_id)
            short_content = generate_short_content(scrape_object.content)
            text = []
            text.append(short_content)
            content = json.dumps(text)
            data = {'short_content': content, 'status' : 'Trends Ready'}
            for key, value in data.items():
                if hasattr(scrape_object, key):
                    setattr(scrape_object, key, value)
            scrape_object.save()
                                        
        logger.warning("Generate Short Content Task Ended")
        return None

    except Exception as e:
        logger.warning(f'Generate Short Content Task Exception {e}')
        return None

@logger.catch
@shared_task
def generate_realated_trend_task():
    logger.warning("Generate Related Trends Task Started")
    try:
        if Scrape.objects.filter(status="Trends Ready"):
            scrape_object = Scrape.objects.filter(status="Trends Ready").order_by('id').first()
            print("check1")
            trending_object = Trending.objects.get(id=scrape_object.trending_id)
            print("check2")
            short_content = generate_trend_topics(scrape_object.content, trending_object.topic)
            print("check3")
            related_topics_rising = []
            related_topics_top = []
            related_queries_rising = []
            related_queries_top = []
            related_queries_rising = split_text(short_content, "Rising Related Queries", "Top Related Queries")
            print("check4")
            related_queries_top = split_text(short_content, "Top Related Queries", "Rising Related Topics")
            related_topics_rising = split_text(short_content, "Rising Related Topics", "Top Related Topics")
            related_topics_top = split_text(short_content, "Top Related Topics", None)
            print("check5")
            print("related_queries_rising",related_queries_rising)
            print("related_queries_top",related_queries_top)
            print("related_topics_rising",related_topics_rising)
            print("related_queries_top",related_topics_top)
            if related_queries_rising or related_queries_top or related_topics_rising or related_topics_top:
                data = {'related_topics_rising' : json.dumps(related_topics_rising), 'related_topics_top' : json.dumps(related_topics_top), 'related_query_rising' : json.dumps(related_queries_rising),
                                        'related_query_top' : json.dumps(related_queries_top), 'status' : 'Content Ready'}
                for key, value in data.items():
                    if hasattr(trending_object, key):
                        setattr(trending_object, key, value)
                trending_object.save()
                print("check6")
                data = {'status' : 'Content Ready'}
                for key, value in data.items():
                    if hasattr(scrape_object, key):
                        setattr(scrape_object, key, value)
                scrape_object.save()
                print("check7")
            else:
                data = {'related_topics_rising' : json.dumps(related_topics_rising), 'related_topics_top' : json.dumps(related_topics_top), 'related_query_rising' : json.dumps(related_queries_rising),
                                        'related_query_top' : json.dumps(related_queries_top), 'status' : 'Blocked'}
                for key, value in data.items():
                    if hasattr(trending_object, key):
                        setattr(trending_object, key, value)
                trending_object.save()
                print("check6")
                data = {'status' : 'Blocked'}
                for key, value in data.items():
                    if hasattr(scrape_object, key):
                        setattr(scrape_object, key, value)
                scrape_object.save()
                print("check7")
                                        
        logger.warning("Generate Related Trends Task Ended")
        return None

    except Exception as e:
        logger.warning(f'Generate Related Trends Task Exception {e}')
        return None


@logger.catch
@shared_task
def generate_content_info_task():
    logger.warning("Generate Content Info Task Started")
    try:
        if Scrape.objects.filter(status="Content Ready"):
            scrape_object = Scrape.objects.filter(status="Content Ready").order_by('id').first()
            short_content = []
            content = []
            logger.warning("Gchecking error d")
            short_content = [item for item in json.loads(scrape_object.title)] + [item for item in json.loads(scrape_object.short_content)]
            logger.warning("check error 12 ed")
            content = [item for item in json.loads(scrape_object.title)] + [item for item in json.loads(scrape_object.content)]
            category = []
            subcategory = []
            tags = []

            generate_post_content_info = generate_content_info(short_content)
            if generate_post_content_info == "":
                scrape_object.status = "Content Blocked"
                scrape_object.save()
            else:
                category = split_text(generate_post_content_info, "Category", "Sub Category")
                subcategory = split_text(generate_post_content_info, "Sub Category", "Tags")
                tags = split_text(generate_post_content_info, "Tags", None)
                print("check 45454")
                if Post.objects.filter(post_id = scrape_object.trending_id).exists():
                    logger.warning("Post Item already exists")
                else:
                    print("check 45450004")
                    post_object = Post(post_id = scrape_object.trending_id,
                                        title = "NoNE",
                                        subtitle = "NoNE",
                                        meta = "NoNE",
                                        content = json.dumps(content),
                                        conclusion = "NoNE",
                                        category = json.dumps(category),
                                        subcategory = json.dumps(subcategory),
                                        tags = json.dumps(tags),
                                        author = "NoNE",
                                        status = "Pre Content",
                                        image_prompt = "NoNE",
                                        image_path = "NoNE",
                                        image_data = "NoNE")
                    post_object.save()
                    scrape_object.status = "Joined"
                    scrape_object.save()
        logger.warning("Generate Content Info Task Ended")
        return None
    except Exception as e:
    #     # Handle any exceptions that may occur
        logger.warning(f'Generate Content Info Task Exception {e}')
        return None

@logger.catch
@shared_task
def generate_content_task():
    logger.warning("Generate Content Task Started")
    try:
        if Post.objects.filter(status="Pre Content"):
            post_object = Post.objects.filter(status= "Pre Content").order_by('id').first()
            topics_object = Trending.objects.get(id= post_object.post_id)
            scrape_object = Scrape.objects.get(trending_id = post_object.post_id)
            related_topic = json.loads(topics_object.related_topics_rising) + json.loads(topics_object.related_topics_top)
            related_query = json.loads(topics_object.related_query_rising) + json.loads(topics_object.related_query_top)
            content = json.loads(post_object.content)

            generate_post_content, author_name = generate_content(topics_object.topic,scrape_object.short_content, content, related_topic, related_query, json.loads(post_object.category))
            questions_list=[]
            questions_list = generate_content_cta(generate_post_content)
            cleaned_heading = []
            cleaned_subheading = []
            cleaned_content = []
            cleaned_conclusion = []
            cleaned_heading = split_text(generate_post_content, "Heading", "Introduction")
            cleaned_subheading = split_text(generate_post_content, "Introduction", "Body")
            cleaned_content = split_text(generate_post_content, "Body", "Conclusion")
            cleaned_conclusion = split_text(generate_post_content, "Conclusion", None)
            
            if cleaned_heading == "" or cleaned_subheading == "" or cleaned_content == "" or cleaned_conclusion == "":
                data = {'title': 'none', 'subtitle': 'none', 'content': 'none', 'conclusion': 'none', 'author': author_name, 'status' : 'Content Issue'}
                for key, value in data.items():
                    if hasattr(post_object, key):
                        setattr(post_object, key, value)
                post_object.save()
            else:
                data = {'title': json.dumps(cleaned_heading), 'subtitle': json.dumps(cleaned_subheading), 'content': json.dumps(cleaned_content), 'conclusion': json.dumps(cleaned_conclusion), 'author': author_name, 'status' : 'Post Content', 'survey' : questions_list}
                for key, value in data.items():
                    if hasattr(post_object, key):
                        setattr(post_object, key, value)
                post_object.save()
            logger.warning("Generate Content Task Ended")
            return None
    except Exception as e:
        logger.warning(f'Generate Content Task Exception {e}')
        return None

@logger.catch
@shared_task
def generate_image_prompt_task():
    logger.warning("Generate Image Prompt Task Started")
    try:
        if Post.objects.filter(status = "Post Content"):
            post_object = Post.objects.filter(status = "Post Content").order_by('id').first()
            image_prompt = []
            image_prompt_content = [item for item in json.loads(post_object.content)] + [item for item in json.loads(post_object.conclusion)]
            image_prompt = generate_image_prompt(image_prompt_content)
            data = {'image_prompt': image_prompt, 'status' : 'ImageGenReady'}

            for key, value in data.items():
                if hasattr(post_object, key):
                    setattr(post_object, key, value)
            post_object.save()
            logger.warning("Generate Image Prompt Task Completed")
            return None
    except Exception as e:
        logger.warning(f'Generate Image Prompt Task Exception {e}')
        return None

@logger.catch
@shared_task
def generate_image_task():
    logger.warning("Generate Image Task Started")
    try:
        if Post.objects.filter(status = "ImageGenReady"):
            post_object = Post.objects.filter(status = "ImageGenReady").order_by('id').first()
            logger.warning("Generate Image Task Working")
            logger.warning("Gener345r6t5fe4def5rorking")
            crm_path, image_path, base64_image = asyncio.run(generate_image_api(post_object.image_prompt, post_object.id))
            logger.warning("efrgthyuj654567orking")
            image_data = []
            image_data.append(post_object.image_prompt)
            image_data.append(str(crm_path))
            image_data.append(str(image_path))
            image_data.append(base64_image)
            all_image_datas = []
            all_image_datas.append(image_data)
            all_image_data = json.dumps(all_image_datas)
            data = {'image_crm' : crm_path, 'image_path' : image_path, 'all_image_data' : all_image_data, 'image_data' : base64_image,'status' : 'Meta Ready'}

            for key, value in data.items():
                if hasattr(post_object, key):
                    setattr(post_object, key, value)
            post_object.save()
            logger.warning("Generate Image Task Ended")
            return None
    except Exception as e:
    #     # Handle any exceptions that may occur
        logger.warning(f'Generate Image Task Exception {e}')
        return None

@logger.catch
@shared_task
def generate_meta_info_task():
    logger.warning("Generate Meta Task Started")
    try:
        if Post.objects.filter(status="Meta Ready"):
            post_object = Post.objects.filter(status="Meta Ready").order_by('id').first()
            trending_object = Trending.objects.get(id = post_object.post_id)
            related_topics_rising = json.loads(trending_object.related_topics_rising)
            related_topics_top = json.loads(trending_object.related_topics_top)
            related_query_rising = json.loads(trending_object.related_query_rising)
            related_query_top = json.loads(trending_object.related_query_top)
            related_topics = related_topics_rising + related_topics_top
            related_query= related_query_rising + related_query_top
            meta = generate_meta_info(related_topics,related_query,post_object.content)
            data = {'meta': meta, 'status' : 'Draft'}
            for key, value in data.items():
                if hasattr(post_object, key):
                    setattr(post_object, key, value)
            post_object.save()
                                        
        logger.warning("Generate Meta Task Ended")
        return None

    except Exception as e:
        logger.warning(f'Generate Meta Task Exception {e}')
        return None


@logger.catch
@shared_task
def fetch_api_website():
    logger.warning("API hit Website Started")
    # Define the URL of the API endpoint you want to hit
    api_url = "http://tewsletter.com/api/postapi/saved/"
    
    try:
        # Make a GET request to the API endpoint
        response = requests.get(api_url)
        data = response.json()
        if response.status_code == 200:
            logger.warning("API hit successful!")
            for item in data:
                
                if Post.objects.filter(post_id=item['post_id']).exists():
                    
                    post_object = Post.objects.get(post_id=item['post_id'])
                    post_object.status = "Sent"
                    post_object.save()
                    logger.warning("API Table Saved")
                else:
                    logger.warning("API post does not exist")
        else:
            logger.warning(f"API hit failed with status code {response.status_code}")
    except Exception as e:
        logger.warning(f'API hit successful! Exception {e}')


################################## Regenrate Task Functions ####################################

@logger.catch
@shared_task
def regenerate_content_task(id):
    logger.warning("Regenerate Content Task Started")
    try:
        post_object = Post.objects.get(post_id = id)
        scrape_object = Scrape.objects.get(trending_id = id)
        logger.warning("Regenerate Content Task Working")
        content = [item for item in scrape_object.title] #+ [item for item in scrape_object.content]
        generate_post_content_info = generate_content_info(content)
        category = []
        subcategory = []
        tags = []
        category = split_text(generate_post_content_info, "Category", "Sub Category")
        subcategory = split_text(generate_post_content_info, "Sub Category", "Tags")
        tags = split_text(generate_post_content_info, "Tags", None)

        topics_object = Trending.objects.get(id = post_object.post_id)
        
        related_topic = json.loads(topics_object.related_topics_rising) + json.loads(topics_object.related_topics_top)
        related_query = json.loads(topics_object.related_query_rising) + json.loads(topics_object.related_query_top)
        
        generate_post_content, author_name = generate_content(json.loads(topics_object.topic), content, related_topic, related_query, category)
        questions_list = []
        
        questions_list = generate_content_cta(generate_post_content)
        
        cleaned_heading = []
        cleaned_subheading = []
        cleaned_content = []
        cleaned_conclusion = []
        cleaned_heading = split_text(generate_post_content, "Heading", "Introduction")
        cleaned_subheading = split_text(generate_post_content, "Introduction", "Body")
        cleaned_content = split_text(generate_post_content, "Body", "Conclusion")
        cleaned_conclusion = split_text(generate_post_content, "Conclusion", None)
        
        if cleaned_heading == "" or cleaned_subheading == "" or cleaned_content == "" or cleaned_conclusion == "":
            data = {'category': category, 'subcategory' : subcategory, 'tags' : tags, 'title': 'none', 'subtitle': 'none', 'content': 'none', 'conclusion': 'none', 'author': author_name, 'status' : 'Content Issue'}
            for key, value in data.items():
                if hasattr(post_object, key):
                    setattr(post_object, key, value)
            post_object.save()
        else:
            data = {'category': json.dumps(category), 'subcategory' : json.dumps(subcategory), 'tags' : json.dumps(tags), 'title': json.dumps(cleaned_heading), 'subtitle': json.dumps(cleaned_subheading), 'content': json.dumps(cleaned_content), 'conclusion': json.dumps(cleaned_conclusion), 'author': author_name, 'status' : 'Content Regenerated', 'survey' : json.dumps(questions_list)}
            for key, value in data.items():
                if hasattr(post_object, key):
                    setattr(post_object, key, value)
            post_object.save()

        return None
    except Exception as e:
    #     # Handle any exceptions that may occur
        logger.warning(f'Regenerate Content Task Working {e}')
        return None
     
@logger.catch
@shared_task    
def regenerate_image_task(id):
    logger.warning("Regenerate Image Task Working")
    try:
        post_object = Post.objects.get(post_id=id)

        image_prompt_content = [item for item in json.loads(post_object.content)] + [item for item in json.loads(post_object.conclusion)]
        image_prompt = []
        image_prompt = generate_image_prompt(image_prompt_content)
        
        crm_path, image_path, base64_image = asyncio.run(generate_image_api(json.loads(post_object.image_prompt), post_object.id))
        image_data = []
        image_data.append(image_prompt)
        image_data.append(str(crm_path))
        image_data.append(str(image_path))
        image_data.append(base64_image)
        
        all_image_datas = []
        
        all_image_datas = json.loads(post_object.all_image_data)
        all_image_datas.append(image_data)
        all_image_data = json.dumps(all_image_datas)
        

        data = {'image_crm' : crm_path, 'image_path' : image_path, 'all_image_data' : json.dumps(all_image_data), 'image_data' : base64_image,'status' : 'Draft'}

        for key, value in data.items():
            if hasattr(post_object, key):
                setattr(post_object, key, value)
        post_object.save()
        logger.warning("Regenerate Image Task Ended")
        return None
    except Exception as e:
    #     # Handle any exceptions that may occur
        logger.warning(f'Regenerate Image Task Exception {e}')
        return None

################################## Functions ####################################
########################################## Pytrends Function Starts #####################################################

# @logger.catch
# def get_related_query(related, data):
#     related_rising =[]
#     related_top=[]
#     try:
#         # Check if 'rising' key exists and has data
#         if 'rising' in related[data] and not related[data]['rising'].empty:
#             related_rising.extend(related[data]['rising']['query'])

#         # Check if 'top' key exists and has data
#         if 'top' in related[data] and not related[data]['top'].empty:
#             related_top.extend(related[data]['top']['query'])
   
#     except Exception as e:
#         logger.warning(f'Get Related Query Exception {e}')
#         pass  # Skip if any error occurs
    
#     return related_rising,related_top  

# @logger.catch
# def get_related_topic(related, data):
#     related_rising =[]
#     related_top=[]
#     try:
#         # Check if 'rising' key exists and has data
#         if 'rising' in related[data] and not related[data]['rising'].empty:
#             related_rising.extend(related[data]['rising']['topic_title'])

#         # Check if 'top' key exists and has data
#         if 'top' in related[data] and not related[data]['top'].empty:
#             related_top.extend(related[data]['top']['topic_title'])
   
#     except Exception as e:
#         logger.warning(f'Get Related Topic Exception {e}')
#         pass  # Skip if any error occurs
    
#     return related_rising,related_top  

########################################## Pytrends Function Ends #####################################################

##################################  Twitter Post Functions ####################################

@logger.catch
@shared_task
def generate_twitter_post_task():

    try:
        if Post.objects.filter(status = "Twitter Ready").exists():
            post_object = Post.objects.filter(status = "Twitter Ready").order_by('id').first()
            
            Tweet_content = generate_twitter_post(post_object.conclusion)
            logger.warning("Generate_twitter_post", Tweet_content)
            Tweet_content = []
            Tweet_content=split_text(Tweet_content,"Tweet",None)
            logger.warning("Generate_twitter_post", Tweet_content)
            twitter_object = TwitterPost(post_id = post_object.id,
                                         content= json.dumps(Tweet_content),
                                         status = "Tweet Saved")
            twitter_object.save()
            logger.warning("Generate_twitter_table updated")
            post_object.status = "Draft"
            post_object.save()
            logger.warning("Generate_twitter_post table updated")
            return None
    except Exception as e:
    #     # Handle any exceptions that may occur
        logger.warning(f'Generate_twitter_post Exception {e}')
        return None

@logger.catch
@shared_task
def publish_twitter_post_task():
    try:
        if TwitterPost.objects.filter(status = "Tweet Saved").exists():
            twitter_object = TwitterPost.objects.filter(status = "Tweet Saved").order_by('id').first()
            
            twitter_client = tweepy.Client(consumer_key = "n6WhBu3WFF3OU0qwEDwD1Zrza",
                                           consumer_secret = "kjvqKWucaPNfFAFhT8y1HdbDFr00uiIHqU1uQ6gPCsCh6MznJ8",
                                           access_token = "1784831051531243520-GlRNKbdW59CgM2hm91MJUn5JyaY2t2",
                                           access_token_secret = "ZWrMnCCUyouuWxYkxEGW3rws3pL8SACvR7jW8Pl1EZEVx")
            
            twitter_client.create_tweet(text = json.loads(twitter_object.content))

            data = {'status' : 'Tweet Published'}
            for key, value in data.items():
                if hasattr(twitter_object, key):
                    setattr(twitter_object, key, value)
            twitter_object.save()
            logger.warning("Generate_twitter table updated")
            return None
    except Exception as e:
    #     # Handle any exceptions that may occur
        logger.warning(f'Generate_twitter_post Exception {e}')
        return None

@logger.catch
def generate_twitter_post(merged_content):
    logger.warning("Generate_twitter post started")
    
    genai.configure(api_key="AIzaSyAZLlvQ2yyZxQ6WqfZ0uTBKIhVxU0c-Ml8")
    model = genai.GenerativeModel('gemini-pro')

    post_prompt = """
      {}
        For the above provided Content create a tweet for me following the below instructions
        1. Briefly describe the content you want to tweet about. What are the key points or main idea?
        2. Who are you trying to reach with your tweet? Knowing your audience can help tailor the tone and content. (e.g., Developers, Marketing professionals, General audience)
        3. Do you want to ask a question, spark a conversation, or simply share information? This can influence the tone and phrasing of your tweet.
        4. Are there any relevant hashtags you want to include to increase reach? (e.g., #MachineLearning, #ContentMarketing)
        5. Do you want people to learn more, visit a link, or take any specific action?
        6. Tweet must be less than 280 characters otherwise it is not a tweet

        Here's an example for output tweet :
        Tweet : Fascinated by the potential of AI in content creation!  Could it be a game-changer for marketers?   #ContentMarketing #AI
            """.format(merged_content)

    prompt_content_response = model.generate_content(post_prompt, safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        })

    if prompt_content_response.candidates:
        pre_post_content = prompt_content_response.candidates[0].content.parts[0].text
    else:
        pre_post_content = ""
    return pre_post_content