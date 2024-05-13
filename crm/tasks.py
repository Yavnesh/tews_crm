import os, json,requests
from crm.models import Scrape, Post, TwitterPost, Trending
from crm.fun_gemini import generate_image_prompt, generate_content_info, generate_content, split_text, generate_content_cta,generate_meta_info
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

########################### Gemini Tasks ######################################################
# #Create scrape_url Task every 1 min
schedule, created = IntervalSchedule.objects.get_or_create(every=100, period=IntervalSchedule.SECONDS )

#Schedule the periodic task programmatically

# PeriodicTask.objects.get_or_create(
#     interval = schedule,
#     name = 'generate_content_info_task_periodic',
#     task = 'crm.tasks.generate_content_info_task',
# )

# PeriodicTask.objects.get_or_create(
#     interval = schedule,
#     name = 'generate_content_task_periodic',
#     task = 'crm.tasks.generate_content_task',
# )

# PeriodicTask.objects.get_or_create(
#     interval = schedule,
#     name = 'generate_meta_info_task_periodic',
#     task = 'crm.tasks.generate_meta_info_task',
# )

# PeriodicTask.objects.get_or_create(
#     interval = schedule,
#     name = 'generate_image_prompt_task_periodic',
#     task = 'crm.tasks.generate_image_prompt_task',
# )

# PeriodicTask.objects.get_or_create(
#     interval = schedule,
#     name = 'generate_twitter_post_task_periodic',
#     task = 'crm.tasks.generate_twitter_post_task',
# )

# PeriodicTask.objects.get_or_create(
#     interval = schedule,
#     name = 'fetch_api_website_task_periodic',
#     task = 'crm.tasks.fetch_api_website',
# )

# ########################### Twitter Tasks ######################################################

# PeriodicTask.objects.get_or_create(
#     interval = schedule,
#     name = 'publish_twitter_post_task_periodic',
#     task = 'crm.tasks.publish_twitter_post_task',
# )

# ########################### Horde Tasks ######################################################

# # #Create scrape_url Task every 10 min
# schedule1, created1 = IntervalSchedule.objects.get_or_create(every=360, period=IntervalSchedule.SECONDS )

# PeriodicTask.objects.get_or_create(
#     interval = schedule1,
#     name = 'generate_image_task_periodic',
#     task = 'crm.tasks.generate_image_task',
# )

########################### PyTrend Tasks ######################################################
# # #Create scrape_url Task every 30 min
schedule2, created2 = IntervalSchedule.objects.get_or_create(every=1800, period=IntervalSchedule.SECONDS )
schedule3, created3 = IntervalSchedule.objects.get_or_create(every=900, period=IntervalSchedule.SECONDS )


PeriodicTask.objects.get_or_create(
    interval = schedule2,
    name = 'fetch_trends_task_periodic',
    task = 'crm.tasks.fetch_trends_task',
)

PeriodicTask.objects.get_or_create(
    interval = schedule3,
    name = 'fetch_trends_realtime_task_periodic',
    task = 'crm.tasks.fetch_trends_task',
)

########################### GNews Tasks ######################################################

PeriodicTask.objects.get_or_create(
    interval = schedule,
    name = 'fetch_article_data_task_periodic',
    task = 'crm.tasks.fetch_article_data_task',
)


################################## Gemini Settings ####################################

genai.configure(api_key="AIzaSyBJaCAFmsYpMcO7OTNEJV6I-Ci9O7-X03Q")
model = genai.GenerativeModel('gemini-pro')

safety_setting={
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

################################## Task Functions ####################################
@shared_task
def fetch_trends_task():
    i=0
    print("Fetch Trends Task Started")
    try:
        print("check 1------------------------")
        # connect to google
        pytrends = TrendReq(hl='en-US', tz=360)
        print("check 2------------------------")
        TrendingList = pytrends.trending_searches(pn='united_states')
        print("check 3------------------------")
        trending_list = TrendingList.values.tolist()
        print("check 4------------------------", trending_list)
        topic_list = [item for sublist in trending_list for item in sublist]
        
        for item in topic_list:
            print("for 1------------------------")
            if not Trending.objects.filter(topic = item):
                i = i + 1
                pytrends.build_payload([item], cat=0, timeframe='today 5-y', geo='US', gprop='')

                related_topics = pytrends.related_topics()
                related_query = pytrends.related_queries()

                related_topics_rising, related_topics_top = get_related_topic(related_topics,item)
                related_queries_rising, related_queries_top = get_related_query(related_query,item)
                print("saving to table 1------------------------",related_topics, "***********************", related_query, "***********************",related_topics_rising, "***********************",related_queries_rising)
                trending_object = Trending(topic = item,
                                        related_topics_rising = json.dumps(related_topics_rising),
                                        related_topics_top = json.dumps(related_topics_top),
                                        related_query_rising = json.dumps(related_queries_rising),
                                        related_query_top = json.dumps(related_queries_top),
                                        status = "Saved")
                trending_object.save()
                print("save complete")
                if i >= 5:
                    break
        print("Fetch Trends Task Ended")
        return None

    except Exception as e:
        print(e)
        return None

@shared_task
def fetch_trends_realtime_task():
    print("Fetch Trends Real Time Task Started")
    try:
        # connect to google
        pytrends = TrendReq(hl='en-US', tz=360)
        TrendingList = pytrends.realtime_trending_searches(pn='US')
        topic_list = TrendingList['entityNames'].tolist()
        i = 0
        
        for item in topic_list:
            print("item", item)
            for t in item:
                print("for 2----------------------")
                if not Trending.objects.filter(topic = item):
                    i = i+1
                    pytrends.build_payload([t], cat=0, timeframe='now 1-d', geo='US', gprop='')

                    related_topics = pytrends.related_topics()
                    related_query = pytrends.related_queries()

                    related_topics_rising, related_topics_top = get_related_topic(related_topics,t)
                    related_queries_rising, related_queries_top = get_related_query(related_query,t)
                    print("saving to table 1------------------------",related_topics, "***********************", related_query, "***********************",related_topics_rising, "***********************",related_queries_rising)
                    trending_object = Trending(topic = t,
                                            related_topics_rising = json.dumps(related_topics_rising),
                                            related_topics_top = json.dumps(related_topics_top),
                                            related_query_rising = json.dumps(related_queries_rising),
                                            related_query_top = json.dumps(related_queries_top),
                                            status = "Saved")
                    trending_object.save()
                    print("save complete")
            if i >= 10:
                break
        print("Fetch Trends Real Time Task Ended")
        return None

    except Exception as e:
        print(e)
        return None
    
@shared_task
def fetch_article_data_task():
    print("Fetch Article Data Task Started")
    try:
        if Trending.objects.filter(status = "Saved"):
            trending_object = Trending.objects.filter(status = "Saved").order_by('id').first()
            if not Scrape.objects.filter(trending_id = trending_object.id):
                google_news = GNews()
                json_resp = google_news.get_news(trending_object.topic)

                items = 0
                title = []
                text = []
                images = []
                url = []
                
                config = Config()
                config.request_timeout = 20
                for item in json_resp:
                    url_path = item['url']
                    article = newspaper.Article(url=item['url'], config=config)
                    try:
                        article.download()
                        try:
                            article.parse()
                            img = []
                            for item in article.images:
                                img.append(str(item))
                            title.append(article.title)
                            text.append(article.text)
                            images.append(img)
                            url.append(url_path)
                            
                            items = items + 1
                            if items == 5:
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

                if not Scrape.objects.filter(trending_id = trending_object.id):
                    scrape_object = Scrape( trending_id = trending_object.id,
                                        title = title,
                                        content = content,
                                        images = images,
                                        url = url,
                                        status = "Scraped")
                    scrape_object.save()
                    trending_object.status = "Scraped"
                    trending_object.save()
        print("Fetch Article Data Task Completed")
        return None

    except Exception as e:
        print(e)
        return None

@shared_task
def generate_meta_info_task():
    print("Generate Meta Task Started")
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
                                        
        print("Generate Meta Task Ended")
        return None

    except Exception as e:
        print(e)
        return None


@shared_task
def generate_content_info_task():
    print("Generate Content Info Task Started")
    try:
        if Scrape.objects.filter(status="Scraped"):
            scrape_object = Scrape.objects.filter(status="Scraped").order_by('id').first()

            content = []
            content = [item for item in json.loads(scrape_object.title)] + [item for item in json.loads(scrape_object.content)]
            category = []
            subcategory = []
            tags = []

            generate_post_content_info = generate_content_info(content)
            if generate_post_content_info == "":
                scrape_object.status = "Content Blocked"
                scrape_object.save()
            else:
                category = split_text(generate_post_content_info, "Category", "Sub Category")
                subcategory = split_text(generate_post_content_info, "Sub Category", "Tags")
                tags = split_text(generate_post_content_info, "Tags", None)
            
                if not Post.objects.filter(post_id = scrape_object.trending_id):
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
        print("Generate Content Info Task Ended")
        return None
    except Exception as e:
    #     # Handle any exceptions that may occur
        print(e)
        return None

@shared_task
def generate_content_task():
    print("Generate Content Task Started")
    try:
        if Post.objects.filter(status="Pre Content"):
            post_object = Post.objects.filter(status= "Pre Content").order_by('id').first()
            topics_object = Trending.objects.get(id= post_object.post_id)
            related_topic = json.loads(topics_object.related_topics_rising) + json.loads(topics_object.related_topics_top)
            related_query = json.loads(topics_object.related_query_rising) + json.loads(topics_object.related_query_top)
            content = json.loads(post_object.content)

            generate_post_content, author_name = generate_content(topics_object.topic,content, related_topic, related_query, json.loads(post_object.category))
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
            print("Generate Content Task Ended")
            return None
    except Exception as e:
        print(e)
        return None

@shared_task
def generate_image_prompt_task():
    print("Generate Image Prompt Task Started")
    try:
        if Post.objects.filter(status = "Post Content"):
            post_object = Post.objects.filter(status = "Post Content").order_by('id').first()
            image_prompt = []
            image_prompt_content = [item for item in json.loads(post_object.content)] + [item for item in json.loads(post_object.conclusion)]
            image_prompt = generate_image_prompt(image_prompt_content)
            data = {'image_prompt': json.dumps(image_prompt), 'status' : 'ImageGenReady'}

            for key, value in data.items():
                if hasattr(post_object, key):
                    setattr(post_object, key, value)
            post_object.save()
            print("Generate Image Prompt Task Completed")
            return None
    except Exception as e:
        print(e)
        return None

@shared_task
def generate_image_task():
    print("Generate Image Task Started")
    try:
        if Post.objects.filter(status = "ImageGenReady"):
            post_object = Post.objects.filter(status = "ImageGenReady").order_by('id').first()
            print("working -----task generate image generation")
            
            crm_path, image_path, base64_image = asyncio.run(generate_image_api(json.loads(post_object.image_prompt), post_object.id))
            image_data = []
            image_data.append(json.loads(post_object.image_prompt))
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
            print("Generate Image Prompt Task Completed.")
            return None
    except Exception as e:
    #     # Handle any exceptions that may occur
        print(e)
        return None

@shared_task
def fetch_api_website():
    # Define the URL of the API endpoint you want to hit
    api_url = "http://tewsletter.com/api/postapi/saved/"
    
    try:
        # Make a GET request to the API endpoint
        response = requests.get(api_url)
        data = response.json()
        if response.status_code == 200:
            print("API hit successful!")
            for item in data:
                print("API sful!", item['post_id'])
                if Post.objects.filter(post_id=item['post_id']).exists():
                    print("t successful!")
                    post_object = Post.objects.get(post_id=item['post_id'])
                    post_object.status = "Sent"
                    post_object.save()
                    print("Table Saved")
                else:
                    print("Taed")
        else:
            print(f"API hit failed with status code {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")


################################## Regenrate Task Functions ####################################

@shared_task
def regenerate_content_task(id):
    try:
        post_object = Post.objects.get(post_id = id)
        scrape_object = Scrape.objects.get(trending_id = id)
        print("working -----task regenerate content")
        content = [item for item in scrape_object.title] #+ [item for item in scrape_object.content]
        print("step 2")
        generate_post_content_info = generate_content_info(content)
        print("step 3")
        category = []
        subcategory = []
        tags = []
        category = split_text(generate_post_content_info, "Category", "Sub Category")
        subcategory = split_text(generate_post_content_info, "Sub Category", "Tags")
        tags = split_text(generate_post_content_info, "Tags", None)
        print("step 11")
        topics_object = Trending.objects.get(id = post_object.post_id)
        print("check step 1", json.loads(topics_object.related_topics_rising))
        related_topic = json.loads(topics_object.related_topics_rising) + json.loads(topics_object.related_topics_top)
        related_query = json.loads(topics_object.related_query_rising) + json.loads(topics_object.related_query_top)
        print("step 13")
        generate_post_content, author_name = generate_content(json.loads(topics_object.topic), content, related_topic, related_query, category)
        questions_list = []
        print("step 14")
        questions_list = generate_content_cta(generate_post_content)
        print("step 18")
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
        print(e)
        return None
     

@shared_task    
def regenerate_image_task(id):
    try:
        print(id)
        post_object = Post.objects.get(post_id=id)
        print("working -----task generate image generation", id)
        image_prompt_content = [item for item in json.loads(post_object.content)] + [item for item in json.loads(post_object.conclusion)]
        image_prompt = []
        image_prompt = generate_image_prompt(image_prompt_content)
        
        crm_path, image_path, base64_image = asyncio.run(generate_image_api(json.loads(post_object.image_prompt), post_object.id))
        image_data = []
        image_data.append(image_prompt)
        image_data.append(str(crm_path))
        image_data.append(str(image_path))
        image_data.append(base64_image)
        print("error hertyuj")
        all_image_datas = []
        
        all_image_datas = json.loads(post_object.all_image_data)
        all_image_datas.append(image_data)
        all_image_data = json.dumps(all_image_datas)
        

        data = {'image_crm' : crm_path, 'image_path' : image_path, 'all_image_data' : json.dumps(all_image_data), 'image_data' : base64_image,'status' : 'Draft'}

        for key, value in data.items():
            if hasattr(post_object, key):
                setattr(post_object, key, value)
        post_object.save()
        return None
    except Exception as e:
    #     # Handle any exceptions that may occur
        print(e)
        return None

################################## Functions ####################################
########################################## Pytrends Function Starts #####################################################

def get_related_query(related, data):
    related_rising =[]
    related_top=[]
    try:
        # Check if 'rising' key exists and has data
        if 'rising' in related[data] and not related[data]['rising'].empty:
            related_rising.extend(related[data]['rising']['query'])

        # Check if 'top' key exists and has data
        if 'top' in related[data] and not related[data]['top'].empty:
            related_top.extend(related[data]['top']['query'])
   
    except Exception as e:
        print(e)
        pass  # Skip if any error occurs
    
    return related_rising,related_top  

def get_related_topic(related, data):
    related_rising =[]
    related_top=[]
    try:
        # Check if 'rising' key exists and has data
        if 'rising' in related[data] and not related[data]['rising'].empty:
            related_rising.extend(related[data]['rising']['topic_title'])

        # Check if 'top' key exists and has data
        if 'top' in related[data] and not related[data]['top'].empty:
            related_top.extend(related[data]['top']['topic_title'])
   
    except Exception as e:
        print(e)
        pass  # Skip if any error occurs
    
    return related_rising,related_top  

########################################## Pytrends Function Ends #####################################################

##################################  Twitter Post Functions ####################################

@shared_task
def generate_twitter_post_task():

    try:
        if Post.objects.filter(status = "Twitter Ready"):
            post_object = Post.objects.filter(status = "Twitter Ready").order_by('id').first()
            
            Tweet_content = generate_twitter_post(post_object.conclusion)
            print("generate_twitter_post(post_object.conclusion)",Tweet_content)
            Tweet_content = []
            Tweet_content=split_text(Tweet_content,"Tweet",None)
            print("working -----twitter post", Tweet_content)
            twitter_object = TwitterPost(post_id = post_object.id,
                                         content= json.dumps(Tweet_content),
                                         status = "Tweet Saved")
            twitter_object.save()
            post_object.status = "Draft"
            post_object.save()
            return None
    except Exception as e:
    #     # Handle any exceptions that may occur
        print(e)
        return None

@shared_task
def publish_twitter_post_task():
    try:
        if TwitterPost.objects.filter(status = "Tweet Saved"):
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
            return None
    except Exception as e:
    #     # Handle any exceptions that may occur
        print(e)
        return None
    
def generate_twitter_post(merged_content):
    print("working -----twitter post api",os.environ.get('Gemini_API_key'))
    genai.configure(api_key="AIzaSyDUvhzuC5-xrgN1pVXc9knhGlv30sLlw34")
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
