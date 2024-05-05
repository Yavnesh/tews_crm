from celery import shared_task
# from django.db import models
from crm.models import Scrape, Post, TwitterPost, Trending
from crm.function_gemini import generate_image_prompt, generate_content_info, generate_content
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re, random, string, os, tweepy
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
# from horde_client import HordeClient, ImageGenParams
import io
import base64
from PIL import Image
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import asyncio
import aiohttp
import time
from pathlib import Path
from horde_sdk import ANON_API_KEY
from horde_sdk.ai_horde_api import AIHordeAPIAsyncManualClient
from horde_sdk.ai_horde_api.apimodels import ImageGenerateAsyncRequest, ImageGenerateStatusRequest
from horde_sdk.generic_api.apimodels import RequestErrorResponse


from gnews import GNews
import requests
import pandas as pd
from pytrends.request import TrendReq
import newspaper
from newspaper import Config, Article, Source


# #Create scrape_url Task every 1 min
schedule, created = IntervalSchedule.objects.get_or_create(every=300, period=IntervalSchedule.SECONDS )

# #Schedule the periodic task programmatically

PeriodicTask.objects.get_or_create(
    interval = schedule,
    name = 'generate_content_info_task_periodic',
    task = 'crm.tasks.generate_content_info_task',
)

PeriodicTask.objects.get_or_create(
    interval = schedule,
    name = 'generate_content_task_periodic',
    task = 'crm.tasks.generate_content_task',
)

PeriodicTask.objects.get_or_create(
    interval = schedule,
    name = 'generate_image_prompt_task_periodic',
    task = 'crm.tasks.generate_image_prompt_task',
)

PeriodicTask.objects.get_or_create(
    interval = schedule,
    name = 'generate_twitter_post_task_periodic',
    task = 'crm.tasks.generate_twitter_post_task',
)

PeriodicTask.objects.get_or_create(
    interval = schedule,
    name = 'publish_twitter_post_task_periodic',
    task = 'crm.tasks.publish_twitter_post_task',
)

# #Create scrape_url Task every 10 min
schedule1, created1 = IntervalSchedule.objects.get_or_create(every=600, period=IntervalSchedule.SECONDS )

PeriodicTask.objects.get_or_create(
    interval = schedule1,
    name = 'generate_image_task_periodic',
    task = 'crm.tasks.generate_image_task',
)

# # #Create scrape_url Task every 30 min
# schedule2, created2 = IntervalSchedule.objects.get_or_create(every=1800, period=IntervalSchedule.SECONDS )
# schedule3, created3 = IntervalSchedule.objects.get_or_create(every=2000, period=IntervalSchedule.SECONDS )


PeriodicTask.objects.get_or_create(
    interval = schedule1,
    name = 'fetch_trends_task_periodic',
    task = 'crm.tasks.fetch_trends_task',
)

PeriodicTask.objects.get_or_create(
    interval = schedule,
    name = 'fetch_article_data_task_periodic',
    task = 'crm.tasks.fetch_article_data_task',
)

################################## Gemini Settings ####################################

genai.configure(api_key="AIzaSyDUvhzuC5-xrgN1pVXc9knhGlv30sLlw34")
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
    try:
        # connect to google
        pytrends = TrendReq(hl='en-US', tz=360)
        # print(pd.__version__)
        TrendingList = pytrends.trending_searches(pn='united_states')
        # print(TrendingList)
        # trending_list = Trending[0].tolist()
        # print(trending_list[0])
        trending_list = TrendingList.values.tolist()
        # print(trending_list)
        flat_list = [item for sublist in trending_list for item in sublist]
        # print(flat_list)
        for item in flat_list:
            if not Trending.objects.filter(topic = item):
                pytrends.build_payload([item], cat=0, timeframe='today 5-y', geo='US', gprop='')

                related_topics = pytrends.related_topics()
                related_queries = pytrends.related_queries()
                # Related Topics (Rising)
                try:
                    if item in related_topics and 'rising' in related_topics[item] and 'topic_title' in related_topics[item]['rising']:
                        t_rising = related_topics[item]['rising']['topic_title']
                        related_topics_rising = t_rising.values.tolist()


                except (KeyError, AttributeError):
                    pass  # Skip if any error occurs

                # Related Topics (Top)
                try:
                    if item in related_topics and 'top' in related_topics[item] and 'topic_title' in related_topics[item]['top']:
                        t_top = related_topics[item]['top']['topic_title']
                        related_topics_top = t_top.values.tolist()
                except (KeyError, AttributeError):
                    pass  # Skip if any error occurs

                # Related Queries (Rising)
                try:
                    if item in related_queries and 'rising' in related_queries[item] and 'query' in related_queries[item]['rising']:
                        q_rising = related_queries[item]['rising']['query']
                        related_queries_rising = q_rising.values.tolist()
                except (KeyError, AttributeError):
                    pass  # Skip if any error occurs

                # Related Queries (Top)
                try:
                    if item in related_queries and 'top' in related_queries[item] and 'query' in related_queries[item]['top']:
                        q_top = related_queries[item]['top']['query']
                        related_queries_top = q_top.values.tolist()
                except (KeyError, AttributeError):
                    pass  # Skip if any error occurs


                # print("table saved12345678")
                trending_object = Trending(topic = item,
                                        related_topics_rising = related_topics_rising,
                                        related_topics_top = related_topics_top,
                                        related_query_rising = related_queries_rising,
                                        related_query_top = related_queries_top,
                                        status = "Saved")
                trending_object.save()
                print("table saved")
        return None

    except Exception as e:
    #     # Handle any exceptions that may occur
        print(e)
        return None

@shared_task
def fetch_article_data_task():
    try:
        if Trending.objects.filter(status = "Saved"):
            trending_object = Trending.objects.filter(status = "Saved").order_by('id').first()
            if not Scrape.objects.filter(trending_id = trending_object.id):
                google_news = GNews()
                json_resp = google_news.get_news(trending_object.topic)
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
                    # print("i--",i)
                    
                    article = newspaper.Article(url=item['url'], config=config)
                    try:
                        article.download()
                        # print("Article downloaded successfully!")
                        try:
                            article.parse()
                            # print("Article Parsed successfully!")

                            title.append(article.title)
                            text.append(article.text)
                            images.append(article.images)
                            url.append(item['url'])
                            
                            # print("items--",items, "--title--",article.title)
                            # print("items--",items, "--text--",article.text)
                            # print("items--",items, "--images--",article.images)
                            # print("items--",items, "--url--",item['url'])

                            items = items + 1
                            if items == 10:
                                print("break")
                                break

                        except Exception as e:
                            print(e)
                            # print("Article Not Parsed !")

                    except Exception as e:
                        print(e)
                        # print("Article Not Downloaded")

                if not Scrape.objects.filter(trending_id = trending_object.id):
                    scrape_object = Scrape( trending_id = trending_object.id,
                                        title = title,
                                        content = text,
                                        images = images,
                                        url = url,
                                        status = "Scraped")
                    scrape_object.save()
                    trending_object.status = "Scraped"
                    trending_object.save()
        return None

    except Exception as e:
    #     # Handle any exceptions that may occur
        print(e)
        return None

@shared_task
def generate_content_info_task():
    try:
        if Scrape.objects.filter(status="Scraped"):
            scrape_object = Scrape.objects.filter(status="Scraped").order_by('id').first()
            print("working -----task generate content info")
            content = join_post(scrape_object.trending_id)
            print(content)
            generate_post_content_info = generate_content_info(content)
            if generate_post_content_info == "":
                scrape_object.status = "Content Blocked"
                scrape_object.save()
            else:
                # print("generate_post_content_info----------------------------------------", generate_post_content_info)
                category = split_text(generate_post_content_info, "Category", "Sub Category")
                print("category-------------------------------------------------------", category)
                subcategory = split_text(generate_post_content_info, "Sub Category", "Tags")
                print("subcategory-------------------------------------------------------", subcategory)
                tags = split_text(generate_post_content_info, "Tags", None)
                print("tags----------", tags)
                if not Post.objects.filter(post_id = scrape_object.trending_id):
                    post_object = Post(post_id = scrape_object.trending_id,
                                        title = "NoNE",
                                        subtitle = "NoNE",
                                        content = content,
                                        conclusion = "NoNE",
                                        category = category,
                                        subcategory = subcategory,
                                        tags = tags,
                                        author = "NoNE",
                                        status = "Pre Content",
                                        image_prompt = "NoNE",
                                        image_path = "NoNE",
                                        image_data = "NoNE")
                    post_object.save()
                    scrape_object.status = "Joined"
                    scrape_object.save()
        return None
    except Exception as e:
    #     # Handle any exceptions that may occur
        print(e)
        return None

@shared_task
def generate_content_task():
    try:
        # print("generatecontentfffffffffffffffffffffffffffffffffffffffff")
        if Post.objects.filter(status="Pre Content"):
            post_object = Post.objects.filter(status= "Pre Content").order_by('id').first()
            # print("working -----task generate content",post_object.content)
            # print("working -----task generate content",post_object.category)
            generate_post_content, author_name = generate_content(post_object.content, post_object.category)
            # print("content-------758687g--", generate_post_content)
            # print("content-------758687g- author-", author_name)
            cleaned_heading = split_text(generate_post_content, "Heading", "Introduction")
            cleaned_subheading = split_text(generate_post_content, "Introduction", "Body")
            cleaned_content = split_text(generate_post_content, "Body", "Conclusion")
            cleaned_conclusion = split_text(generate_post_content, "Conclusion", None)
            # print("content---------", generate_post_content)
            # print("heading-------1--------",cleaned_heading)
            # print("heading--------2-------",cleaned_subheading)
            # print("heading---------3------",cleaned_content)
            # print("heading---------4------",cleaned_conclusion)
            data = {'title': cleaned_heading, 'subtitle': cleaned_subheading, 'content': cleaned_content, 'conclusion': cleaned_conclusion, 'author': author_name, 'status' : 'Post Content'}

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
def generate_image_prompt_task():
    try:
        if Post.objects.filter(status = "Post Content"):
            post_object = Post.objects.filter(status = "Post Content").order_by('id').first()
            # print("working -----task generate image prompt")
            image_prompt_content = [item for item in post_object.content] + [item for item in post_object.conclusion]
            image_prompt = generate_image_prompt(image_prompt_content)
            data = {'image_prompt': image_prompt, 'status' : 'ImageGenReady'}

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
def generate_image_task():
    try:
        if Post.objects.filter(status = "ImageGenReady"):
            post_object = Post.objects.filter(status = "ImageGenReady").order_by('id').first()
            print("working -----task generate image generation")

            image_path, image_path_static = asyncio.run(generate_image_api(post_object.image_prompt, post_object.id))
            base64_image= base64.b64encode(image_path_static.read_bytes()).decode()
            #Post processing Upscale 

            data = {'image_path' : image_path, 'image_data' : base64_image,'status' : 'Twitter Ready'}

            for key, value in data.items():
                if hasattr(post_object, key):
                    setattr(post_object, key, value)
            post_object.save()
            return None
    except Exception as e:
    #     # Handle any exceptions that may occur
        print(e)
        return None

################################## Regenrate Task Functions ####################################

@shared_task
def regenerate_content_info_task(id):
    try:
        content = join_post(id)
        generate_post_content_info = generate_content_info(content)
        category = split_text(generate_post_content_info, "Category", "Sub Category")
        subcategory = split_text(generate_post_content_info, "Sub Category", "Tags")
        tags = split_text(generate_post_content_info, "Tags", None)
        data = {'category': category, 'subcategory': subcategory, 'tags': tags}
        post_object = Post.objects.get(post_id = id)
        for key, value in data.items():
            if hasattr(post_object, key):
                setattr(post_object, key, value)
        post_object.save()

        # data1 = {'status': 'Content Info Re Generated'}
        # url_object = URL.objects.get(id=post_object.post_id)
        # for key, value in data1.items():
        #     if hasattr(url_object, key):
        #         setattr(url_object, key, value)
        # url_object.save()
        # return None
    except Exception as e:
    #     # Handle any exceptions that may occur
        print(e)
        return None
 
@shared_task
def regenerate_content_task(id):
    try:
        post_object = Post.objects.get(post_id = id)
        # print("working -----task regenerate content")

        generate_post_content, author_name = generate_content(post_object.content, post_object.category)
        cleaned_heading = split_text(generate_post_content, "Heading", "Introduction")
        cleaned_subheading = split_text(generate_post_content, "Introduction", "Body")
        cleaned_content = split_text(generate_post_content, "Body", "Conclusion")
        cleaned_conclusion = split_text(generate_post_content, "Conclusion", None)
        
        data = {'title': cleaned_heading, 'subtitle': cleaned_subheading, 'content': cleaned_content, 'conclusion': cleaned_conclusion, 'author': author_name}

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
def regenerate_image_prompt_task(id):
    try:
        post_object = Post.objects.get(post_id = id)
        print("working -----task generate image prompt")
        image_prompt_content = [item for item in post_object.content] + [item for item in post_object.conclusion]
        image_prompt = generate_image_prompt(image_prompt_content)
        data = {'image_prompt': image_prompt, 'status' : 'ImageGenReady'}

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
        post_object = Post.objects.get(post_id = id)
        print("working -----task generate image generation")

        image_path, image_data = generate_image(post_object.image_prompt, post_object.id)
        data = {'image_path' : image_path, 'image_data' : image_data,'status' : 'Draft'}

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

def website_url(url):
    # Extract site name, category, and subcategory from the URL
    try:
        parsed_url = urlparse(url)
        site_name = parsed_url.netloc

        # Split the path of the URL and get the second component
        path_components = parsed_url.path.split("/")
        category = path_components[2]
        sub_category = path_components[3]

        return site_name, category, sub_category
    except Exception as e:
        # Handle any exceptions that may occur
        return None, None, None

def scrape_url(url_a,site_name):
    # Scrape the content of the URL
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        # Based on the site name, perform specific scraping logic
        if site_name == "www.usatoday.com":
            try:
                driver.get(url_a)
                print("print site -----task------", site_name)
                page_content = driver.page_source
                soup = BeautifulSoup(page_content, 'html.parser')

                heading = soup.find('h1', class_='gnt_ar_hl').text if soup.find('h1', class_='gnt_ar_hl') else ""
                sub_heading = soup.find('h2', class_='gnt_ar_shl').text if soup.find('h2', class_='gnt_ar_shl') else ""
                paragraphs = soup.find_all('p', class_='gnt_ar_b_p')

                content = ''
                for paragraph in paragraphs:
                    # Check if paragraph contains any <a> tags
                    if paragraph.find('a'):
                        continue  # Skip this paragraph if it contains links
                    content += paragraph.text + '\n'
                return heading, sub_heading, content
            finally:
                driver.quit()
        elif site_name == "www.usatoday1.com":
            try:

                driver.get(url_a)
                page_content = driver.page_source
                soup = BeautifulSoup(page_content, 'html.parser')

                heading = soup.find('h1', class_ = 'gnt_ar_hl')
                if not heading:
                    heading = ""
                else:
                    heading = heading.text
                subHeading = soup.find('h2', class_ = 'gnt_ar_shl')
                if not subHeading:
                    subHeading = ""
                else:
                    subHeading = subHeading.text
                paragraphs = soup.find_all('p', class_ = 'gnt_ar_b_p')

                content = ''
                for paragraph in paragraphs:
                    # Check if paragraph contains any <a> tags
                    if paragraph.find('a'):
                        continue  # Skip this paragraph if it contains links
                    content += paragraph.text + '\n'    
                return heading, subHeading, content
            finally:
                driver.quit()
    except Exception as e:
        # Handle any exceptions that may occur
        print(f"Error in scraping URL: {e}")
        return None, None, None

def join_post(id):

    merged_text = ""
    scraped_data = Scrape.objects.get(trending_id = id )
    # print("id------------------",id)
    for data in scraped_data.title:
        merged_text += str(data)
    for data in scraped_data.content:
        merged_text += str(data)
          # Concatenate with spaces

    return merged_text

# def generate_content_info(merged_content):
#     genai.configure(api_key="AIzaSyDUvhzuC5-xrgN1pVXc9knhGlv30sLlw34")
#     model = genai.GenerativeModel('gemini-pro')

#     post_prompt = """
#       {}
#     For the above given blog post 
#         1. Provide a category for this blog post which is best fit to any item in the list.
#         List - [Technology, Entertainment, Automobile, Finance, Health, Fashion, Food, Travel, Environment, Sports, Politics]  
#         If the category does not relate to any item in list then set category as "Other"
#         2. Provide a sub category for this blog post
#         3. Provide 5 very relavent tags for this blog post
#     The output must be in the below given format
#         Category : "One Word Category Name"
#         Sub Category: "One Word Sub Category Name"
#         Tags: "One Word 5 tags in list format"                
#                 """.format(merged_content)

#     prompt_content_response = model.generate_content(post_prompt, safety_settings={
#         HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
#         HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
#         HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
#         HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
#         })

#     if prompt_content_response.candidates:
#         pre_post_content = prompt_content_response.candidates[0].content.parts[0].text
#     else:
#         pre_post_content = ""
#     # print("pre_post_content----------->", pre_post_content)
    
#     return pre_post_content

# def generate_content(merged_content,category):

#     genai.configure(api_key="AIzaSyDUvhzuC5-xrgN1pVXc9knhGlv30sLlw34")
#     model = genai.GenerativeModel('gemini-pro')
#     # print("checking generate content function ----------------",category)
#     author_profile, author_name =  select_author(category)
#     post_prompt = """

#                {} This is an author profile. The author is an expert at writing structured blogs as per his/her personality and charcterstics.
#     The Author uses below format to Structure any blog must be. 
#         1. Craft a Compelling Title/Headline: Introduces the main idea of the article
#         2. Create an Introduction: Tells the reader what the article will be about
#         3. Body: Goes in-depth about the topic of the article. Use Transition Words
#         4. Conclusion: Wraps up the main ideas.
#     Author has given an example also about how to structure a blog post.
#     Example
#         Heading : the heading goes here
#         Introduction : here goes introduction 
#         Body: Here goes body content
#         Conclusion: Here goes conclusion 
                
#                 Understand the below text and write this content as the Author as per the struture and author profile given.
#                 Change the words completely around, make it as it's very different and not the same.
#                 Remove all the credits and authors information from the given content and also, arrange the the content in a way that it does not look like a work of AI.
#                 Also, add some more depth and make it fun as it is going on my blog.
#                 Give me result in 4 parts - heading, intro, body, conclusion.
#                 Keep in mind the content should comply with the safety guidelines of the generative model 
#                 Follow Strictly : Minimum 1000 words
#                 {}
#                 """.format(author_profile, merged_content)

#     prompt_content_response = model.generate_content(post_prompt, safety_settings={
#         HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
#         HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
#         HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
#         HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
#         })

#     if prompt_content_response.candidates:
#         pre_post_content = prompt_content_response.candidates[0].content.parts[0].text
#     else:
#         pre_post_content = ""
#     # print("pre_post_content----------->", pre_post_content)
    
#     return pre_post_content, author_name

# def select_author(category):
#     if category == "Technology":
#         author = """**Name:** Tech Titan Tessa  
#                     **Place:** Silicon Valley  
#                     **Profile:** Hey there, I'm Tech Titan Tessa, your go-to guru for all things tech! Hailing from the innovation hub of Silicon Valley, I've got my finger on the pulse of the latest gadgets, gizmos, and breakthroughs in the world of technology. Whether it's dissecting the newest smartphone release or diving deep into the realms of artificial intelligence, I'm here to decode the digital landscape and keep you ahead of the curve.
#                 """
#         return author, "Tessa"
#     elif category == "Entertainment":
#         author = """**Name:** Entertainment Extraordinaire Ethan  
#                     **Place:** Hollywood  
#                     **Profile:** Lights, camera, action! I'm Ethan, your Entertainment Extraordinaire straight from the heart of Hollywood. With exclusive access to the glitz and glamour of the entertainment industry, I've got the inside scoop on all your favorite celebrities, movies, and TV shows. From red carpet premieres to behind-the-scenes drama, join me for a front-row seat to the world of entertainment!
#                 """
#         return author, "Ethan"
#     elif category == "Automobile":
#         author = """**Name:** Auto Aficionado Alex  
#                     **Place:** Detroit  
#                     **Profile:** Vroom vroom, it's Auto Aficionado Alex here, revving up from the Motor City! As a connoisseur of all things automotive, I'm here to steer you through the fast-paced world of cars, trucks, and everything on wheels. From the latest models to cutting-edge technology, buckle up and join me for a thrilling ride down the highway of automotive news!
#                 """
#         return author, "Alex"
#     elif category == "Finance":
#         author = """**Name:** Financial Whiz Monica  
#                     **Place:** Wall Street  
#                     **Profile:** Welcome to the financial frontier with yours truly, Financial Whiz Monica, reporting live from Wall Street! With a keen eye for market trends and a knack for navigating the complexities of finance, I'm here to guide you through the ever-changing landscape of money matters. From stock market fluctuations to personal finance tips, let's make sense of the numbers together!
#                 """
#         return author, "Monica"
#     elif category == "Health":
#         author = """**Name:** Health Maven Hank  
#                     **Place:** Health Hub  
#                     **Profile:** Hey there, I'm Health Maven Hank, your trusted source for all things wellness! Nestled in the heart of the Health Hub, I've got the latest scoop on fitness trends, medical breakthroughs, and everything in between. Whether you're looking to boost your immune system or stay in tip-top shape, join me on a journey to optimal health and vitality!
#                 """
#         return author, "Hank"
#     elif category == "Fashion":
#         author = """**Name:** Fashionista Fiona  
#                     **Place:** Fashion Capital  
#                     **Profile:** Strike a pose, darlings! It's Fashionista Fiona here, bringing you the hottest trends from the fashion capital of the world. With a flair for style and an eye for couture, I'm your ultimate guide to the runway, the red carpet, and beyond. From haute couture to street style chic, let's explore the ever-evolving world of fashion together!
#                 """
#         return author, "Fiona"
#     elif category == "Food":
#         author = """**Name:** Culinary Connoisseur Carlos  
#                     **Place:** Foodie Haven  
#                     **Profile:** Buen provecho, amigos! I'm Culinary Connoisseur Carlos, your taste bud tour guide through the flavorful world of food. From mouth-watering recipes to culinary adventures from around the globe, join me as we savor the sights, smells, and tastes of gastronomic delight. Whether you're a seasoned chef or a kitchen newbie, let's spice things up together!
#                 """
#         return author, "Carlos"
#     elif category == "Travel":
#         author = """**Name:** Travel Guru Gabby  
#                     **Place:** Wanderlust World  
#                     **Profile:** Bon voyage, fellow explorers! I'm Travel Guru Gabby, your passport to adventure in the wanderlust world. With a thirst for discovery and a love for new horizons, I'm here to whisk you away on unforgettable journeys to far-flung destinations. From hidden gems to bucket-list must-sees, pack your bags and join me for a whirlwind tour of the globe!
#                 """
#         return author, "Gabby"
#     elif category == "Environment":
#         author = """**Name:** Environmental Advocate Eva  
#                     **Place:** Eco Oasis  
#                     **Profile:** Hello, eco-warriors! I'm Environmental Advocate Eva, your voice for planet Earth in the green oasis. With a passion for sustainability and a dedication to preserving our precious natural resources, I'm here to shed light on environmental issues and inspire positive change. From eco-friendly innovations to conservation efforts, let's join forces to protect our planet for future generations!
#                 """
#         return author, "Eva"
#     elif category == "Sports":
#         author = """**Name:** Sports Savant Sam  
#                     **Place:** Sports Central  
#                     **Profile:** Play ball! I'm Sports Savant Sam, your MVP for all things sports in the heart of Sports Central. Whether it's touchdowns or home runs, slam dunks or birdies, I've got the play-by-play coverage and in-depth analysis to keep you on the edge of your seat. So grab your jersey and join me for a front-row seat to the thrilling world of athletics!
#                 """
#         return author, "Sam"
#     elif category == "Politics":
#         author = """**Name:** Political Pundit Pamela  
#                     **Place:** Washington D.C.  
#                     **Profile:** As a seasoned political analyst based in the heart of the nation's capital, I bring you the latest insights and commentary on the ever-changing landscape of American politics. From Capitol Hill to the campaign trail, join me as we navigate the complexities of government, elections, and policy-making.
#                 """
#         return author, "Pamela"
#     else:
#         author = """**Name:** Worldly Wanderer William  
#                     **Place:** Anywhere and Everywhere  
#                     **Profile:** Exploring the wonders of the world, one adventure at a time. From remote villages to bustling metropolises, join me on a journey of discovery and cultural immersion. Let's uncover hidden gems, experience diverse cuisines, and embrace the beauty of our planet.
#                 """
#         return author, "William"

# def generate_image_prompt(merged_content):
#     genai.configure(api_key="AIzaSyDUvhzuC5-xrgN1pVXc9knhGlv30sLlw34")
#     model = genai.GenerativeModel('gemini-pro')

#     post_prompt = """
#       {}

#         For the above provided Article i want to generate a best image prompt for stable diffusion AI model for creating professional digital art.
#         Here are some points you must consider while creating a best image prompt. 
#         1. Analyze the Article:
#             a) Key Concepts and Entities: Identify the main topics, characters, locations, or objects mentioned in the article.
#             b) Visual Style and Setting: Try to understand the overall tone and setting described in the article. Is it a realistic scene, a fantasy world, or something more abstract?
#             c) Action and Details: Pay attention to any actions or specific details that would be visually interesting in an image.

#         2. Craft the Image Prompt: 
#             a) Start with Core Elements: Include the key concepts and entities you identified. Use descriptive language to convey their characteristics.
#                 Example:A photorealistic image of a majestic ancient castle perched on a cliff overlooking a stormy ocean. The castle has tall towers and a long, winding stone bridge leading to its entrance.
#             b) Incorporate Details and Style: Refine the prompt based on the style and setting you identified.
#                 Example (Adding Details and Style): A high-resolution image of a majestic medieval castle perched on a rocky cliff overlooking a stormy ocean at sunset. The castle has tall, round towers with pointed roofs and a long, moss-covered stone bridge leading to its massive wooden gates. Dark storm clouds gather above, casting dramatic shadows on the castle walls.
#             c) Focus on Clarity: Use phrases like "high-resolution," "sharp," or "detailed" to emphasize the desired image quality.
        
#         3. Additional Tips:

#             a) Use References: If the article mentions specific places, objects, or art styles, you can include them in the prompt (e.g., "castle in the style of Hieronymus Bosch").
#             b) Action and Emotion: Consider incorporating actions or emotions of characters to make the image more engaging (e.g., "a knight bravely defending the castle gate").

#             """.format(merged_content)

#     prompt_content_response = model.generate_content(post_prompt, safety_settings={
#         HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
#         HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
#         HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
#         HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
#         })

#     if prompt_content_response.candidates:
#         pre_post_content = prompt_content_response.candidates[0].content.parts[0].text
#     else:
#         pre_post_content = ""
#     # print("image__000__prompt----------->", pre_post_content)
    
#     return pre_post_content

# def generate_image(prompt, id):
#     client = HordeClient(insecure=True)
#     client.clear_model()
#     client.set_model('stable_diffusion')

#     params = ImageGenParams( width = 960, height = 576)
#     # print("prompt---", prompt , "yes")
#     # print("params---", params)
#     image_gen_ouput = client.image_gen(prompt, params=params)

#     # Generate random alphanumeric string
#     chars = string.ascii_lowercase + string.digits
#     random_string = ''.join(random.choice(chars) for _ in range(10))
#     # Combine prefix, random string, and extension
#     file_name = f"{'img_'}{id}_{random_string}.{'png'}"
#     folder_path = "crm/static/crm/img/posts"
#     full_path = os.path.join(folder_path, file_name)
#     img = Image.open(io.BytesIO(base64.decodebytes(bytes(image_gen_ouput.generations[0].img, "utf-8"))))
#     img.save(full_path)
#     image_path = full_path[len("crm/static/"):] 
#     print("Image is saved---")
#     return image_path, image_gen_ouput.generations[0].img

def split_text(text, start_word, end_word):
    # Define the regular expression pattern
    if end_word is not None:
        pattern = re.compile(f'{re.escape(start_word)}(.*?){re.escape(end_word)}', re.DOTALL)
    else:
        pattern = re.compile(f'{re.escape(start_word)}(.*?)$', re.DOTALL)

    # Search for the text between the start and end words
    match = pattern.search(text)
    # print("extracted_text,,,,,,,,,,,,,,,,,,extracted_text")
    if match:
        # Get the text between the start and end words
        extracted_text = match.group(1).strip()
        # print("extracted_text,,,,,,,,,,,,,,,,,",extracted_text)
        if start_word == "Tags":
            items = [item.strip().replace(":", "").replace("*", "").replace("#", "") for item in extracted_text.split(',')]
            tags = []
            for item in items:
                if item:
                    tags.append(item)
            return tags
        elif start_word == "Tweet":
            items = extracted_text.strip().replace(":", "").replace("*", "").replace("-", "")
            return items
        else:
            final_result = []
            text1 = extracted_text.splitlines(False)
            for t in text1:
                result = clean_text(t)
                if result != "":
                    # Add non-empty result to the final result
                    final_result.append(result)
            return final_result
    else:
        return None
    
def clean_text(text):
    # Split the text into words

    words = re.findall(r'\b\w+\b', text)
    
    # Find the index of the first word
    start_index = next((i for i, word in enumerate(words) if word.strip()), None)
    
    # Find the index of the last word
    end_index = next((len(words) - 1 - i for i, word in enumerate(reversed(words)) if word.strip()), None)
    
        # Check if start_index and end_index are None
    if start_index is None or end_index is None:
        return ""
    
    # Extract the substring between the first and last words
    result = ' '.join(words[start_index:end_index + 1]).strip()
    
    # Check if result is None
    if result is None:
        return ""


    # Extract the substring between the first and last words
    result = ' '.join(words[start_index:end_index + 1]).strip()
    
    if text.strip().endswith("."):
        # Add a full stop after the last word
        result += "."
    
    return result

async def generate_image_api(image_prompt, id):
    
    print("Starting...")

    async with aiohttp.ClientSession() as aiohttp_session:
        manual_client = AIHordeAPIAsyncManualClient(aiohttp_session=aiohttp_session)

        image_generate_async_request = ImageGenerateAsyncRequest(
            apikey=ANON_API_KEY,
            prompt=image_prompt,
            models=["Deliberate"],
        )
        print("Submitting image generation request...")
        response = await manual_client.submit_request(
            image_generate_async_request,
            image_generate_async_request.get_default_success_response_type(),
        )

        if isinstance(response, RequestErrorResponse):
            print(f"Error: {response.message}")
            return

        print("Image generation request submitted!")
        image_done = False

        start_time = time.time()
        cycle_time = start_time

        check_counter = 0
        # Keep making ImageGenerateCheckRequests until the job is done.
        while not image_done:
            current_time = time.time()
            if current_time - cycle_time > 20 or check_counter == 0:
                print(f"{current_time - start_time} seconds elapsed ({check_counter} checks made)...")
                cycle_time = current_time

            check_counter += 1
            check_response = await manual_client.get_generate_check(
                job_id=response.id_,
            )

            if isinstance(check_response, RequestErrorResponse):
                print(f"Error: {check_response.message}")
                return

            if check_response.done:
                print("Image is done!")
                print(f"{time.time() - cycle_time} seconds elapsed ({check_counter} checks made)...")

                image_done = True
                break

            await asyncio.sleep(5)

        # Get the image with a ImageGenerateStatusRequest.
        image_generate_status_request = ImageGenerateStatusRequest(
            id=response.id_,
        )

        status_response = await manual_client.submit_request(
            image_generate_status_request,
            image_generate_status_request.get_default_success_response_type(),
        )

        if isinstance(status_response, RequestErrorResponse):
            print(f"Error: {status_response.message}")
            return

        for image_gen in status_response.generations:
            print("Image generation:")
            print(f"ID: {image_gen.id_}")
            print(f"URL: {image_gen.img}")
            #  debug(image_gen)
            print("Downloading image...")

            image_bytes = None
            # image_gen.img is a url, download it using aiohttp.
            async with aiohttp.ClientSession() as session, session.get(image_gen.img) as resp:
                image_bytes = await resp.read()

            if image_bytes is None:
                print("Error: Could not download image.")
                return

            example_path = Path("crm/static/crm/img/posts")
            example_path.mkdir(exist_ok=True, parents=True)

            filepath_to_write_to = example_path / f"{image_gen.id_}_{'img_'}{id}.webp"

            with open(filepath_to_write_to, "wb") as image_file:
                image_file.write(image_bytes)

            print(f"Image downloaded to {filepath_to_write_to}!")
            image_path = filepath_to_write_to[len("crm/static/"):]
            image_path_static = filepath_to_write_to[len("static/"):]

    return image_path, image_path_static

##################################  Twitter Post Functions ####################################

@shared_task
def generate_twitter_post_task():

    try:
        if Post.objects.filter(status = "Twitter Ready"):
            post_object = Post.objects.filter(status = "Twitter Ready").order_by('id').first()
            
            Tweet_content = generate_twitter_post(post_object.conclusion)
            print("generate_twitter_post(post_object.conclusion)",Tweet_content)
            Tweet_content=split_text(Tweet_content,"Tweet",None)
            print("working -----twitter post", Tweet_content)
            twitter_object = TwitterPost(post_id = post_object.id,
                                         content= Tweet_content,
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
            
            twitter_client.create_tweet(text = twitter_object.content)

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
