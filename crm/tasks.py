import os, json,requests
from crm.models import Scrape, Post, TwitterPost, Trending
from crm.clients.genai_client import generate_image_prompt, generate_content_info, generate_content, split_text, generate_content_cta,generate_meta_info, generate_short_content, generate_trend_topics, generate_twitter_post
from crm.clients.horde_client import generate_image_api
from crm.clients.twitter_client import get_twitter_client
##############  Celery  #######################
from celery import shared_task
from django_celery_beat.models import PeriodicTask, IntervalSchedule

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
logger.add("logs/file_task_{time}.log",level="TRACE", rotation="10 MB")
# logger.add("logs/testing.log",level="TRACE", rotation="10 MB")
########################### Periodic Tasks ######################################################
# # Configure logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.WARNING)
# handler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# Interval Schedules
schedules = {
    30: IntervalSchedule.objects.get_or_create(every=30, period=IntervalSchedule.SECONDS),
    60: IntervalSchedule.objects.get_or_create(every=60, period=IntervalSchedule.SECONDS),
    90: IntervalSchedule.objects.get_or_create(every=90, period=IntervalSchedule.SECONDS),
    900: IntervalSchedule.objects.get_or_create(every=900, period=IntervalSchedule.SECONDS),
    1800: IntervalSchedule.objects.get_or_create(every=1800, period=IntervalSchedule.SECONDS),
}

# Periodic Tasks
periodic_tasks = [
    ('generate_short_content_task_periodic', 'crm.tasks.generate_short_content_task', 30),
    ('generate_realated_trend_task_periodic', 'crm.tasks.generate_realated_trend_task', 30),
    ('generate_content_info_task_periodic', 'crm.tasks.generate_content_info_task', 30),
    ('generate_content_task_periodic', 'crm.tasks.generate_content_task', 60),
    ('generate_meta_info_task_periodic', 'crm.tasks.generate_meta_info_task', 30),
    ('generate_image_prompt_task_periodic', 'crm.tasks.generate_image_prompt_task', 30),
    ('fetch_api_website_task_periodic', 'crm.tasks.fetch_api_website', 60),
    ('generate_image_task_periodic', 'crm.tasks.generate_image_task', 90),
    ('fetch_trends_task_periodic', 'crm.tasks.fetch_trends_task', 1800),
    ('fetch_trends_realtime_task_periodic', 'crm.tasks.fetch_trends_realtime_task', 900),
    ('fetch_article_data_task_periodic', 'crm.tasks.fetch_article_data_task', 90),
]

for name, task, interval in periodic_tasks:
    PeriodicTask.objects.get_or_create(
        interval=schedules[interval][0],
        name=name,
        task=task,
    )

################################## Task Functions ####################################


@logger.catch
@shared_task
def fetch_trends_task():
    logger.warning("Fetch Trends Task Started")
    try:
        # connect to google
        pytrends = TrendReq(hl='en-US', tz=360)
        logger.warning("Connected to pytrends")
        
        trending_list = pytrends.trending_searches(pn='united_states').values.tolist()
        topic_list = [item for sublist in trending_list for item in sublist]

        for item in topic_list:
            logger.warning("Processing topic: %s", item)
            if not Trending.objects.filter(topic=item).exists():
                trending_object = Trending(
                    topic=item,
                    related_topics_rising=json.dumps([]),
                    related_topics_top=json.dumps([]),
                    related_query_rising=json.dumps([]),
                    related_query_top=json.dumps([]),
                    source="Daily Trends", 
                    status="Saved"
                )
                trending_object.save()
                logger.warning(f'Table Saved for topic {item}')

        logger.warning("Fetch Trends Task Ended")
    except Exception as e:
        logger.warning(f'Exception in fetch_trends_task: {e}')

@logger.catch
@shared_task
def fetch_trends_realtime_task():
    logger.warning("Fetch Trends Real Time Task Started")
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        logger.warning("Connected to pytrends")

        trending_list = pytrends.realtime_trending_searches(pn='US')['entityNames'].tolist()
        i = 0
        for item in trending_list:
            i = i +1
            logger.warning(f"Processing topic: {item}")
            result = " ".join(item)
            if not Trending.objects.filter(topic=result).exists():
                if i > 3:
                    break
                trending_object = Trending(
                    topic=result,
                    related_topics_rising=json.dumps([]),
                    related_topics_top=json.dumps([]),
                    related_query_rising=json.dumps([]),
                    related_query_top=json.dumps([]),
                    source="Real Time Trends", 
                    status="Saved"
                )
                trending_object.save()
                logger.warning(f'Table Saved for topic {result}')

        logger.warning("Fetch Trends Real Time Task Ended")
    except Exception as e:
        logger.warning(f'Exception in fetch_trends_realtime_task: {e}')

@logger.catch
@shared_task
def fetch_article_data_task():
    """Fetch articles for trending topics and save the data if certain conditions are met."""
    
    logger.warning("Fetch Article Data Task Started")
    try:
        trending_object = Trending.objects.filter(status="Saved").order_by('id').first()
        
        if not trending_object:
            logger.warning("No Trending object with status 'Saved' found.")
            return

        logger.warning(f'Processing trending object with ID {trending_object.id} and topic "{trending_object.topic}"')

        if Scrape.objects.filter(trending_id=trending_object.id).exists():
            logger.warning("Trending item already exists in Scrape table.")
            return

        google_news = GNews()
        json_resp = google_news.get_news(trending_object.topic)
        chr_count, items = 0, 0
        titles, texts, images, urls = [], [], [], []

        config = Config()
        config.request_timeout = 20

        for item in json_resp:
            logger.warning("For loop in Gnews")
            url_path = item['url']
            article = newspaper.Article(url=url_path, config=config)
            try:
                logger.warning("Downloading article...")
                article.download()
                article.parse()
                logger.warning("Article downloaded and parsed successfully.")

                img_list = list(article.images)
                chr_count += len(article.text)

                if chr_count > 50000:
                    logger.warning(f"Character count exceeded limit: {chr_count}")
                    break
                    
                titles.append(article.title)
                texts.append(article.text)
                images.append(img_list)
                urls.append(url_path)
                           
                items += 1
                if items == 10:
                    logger.warning("Reached item limit of 10.")
                    break

            except Exception as e:
                logger.warning(f"Exception occurred while processing article: {e}")
                continue
            
        if titles and texts and urls:
            logger.warning("Collected articles are not empty.")
            if not Scrape.objects.filter(trending_id=trending_object.id).exists():
                if chr_count > 10000:
                    scrape_object = Scrape(
                        trending_id=trending_object.id,
                        title=json.dumps(titles),
                        content=json.dumps(texts),
                        images=json.dumps(images),
                        url=json.dumps(urls),
                        status="Scraped"
                    )
                    scrape_object.save()
                    logger.warning("Scrape object saved.")

                    trending_object.status = "Scraped"
                    trending_object.save()
                    logger.warning("Trending object status updated to 'Scraped'.")
                else:
                    trending_object.status = "Blocked"
                    trending_object.save()
                    logger.warning("Trending object status updated to 'Blocked' due to insufficient content.")
        else:
            trending_object.status = "Blocked"
            trending_object.save()
            logger.warning("No articles were collected.")

        logger.warning("Fetch Article Data Task Completed")

    except Exception as e:
        logger.warning(f"Exception in Fetch Article Data Task: {e}")


@logger.catch
@shared_task
def generate_short_content_task():
    logger.warning("Generate Short Content Task Started")
    try:
        scrape_object = Scrape.objects.filter(status="Scraped").order_by('id').first()
        
        if scrape_object:
            short_content = generate_short_content(scrape_object.content)
            scrape_object.short_content = json.dumps([short_content])
            scrape_object.status = "Trends Ready"
            scrape_object.save()
                                        
        logger.warning("Generate Short Content Task Ended")
    except Exception as e:
        logger.warning(f'Exception in generate_short_content_task: {e}')

@logger.catch
@shared_task
def generate_realated_trend_task():
    logger.warning("Generate Related Trends Task Started")
    try:
        scrape_object = Scrape.objects.filter(status="Trends Ready").order_by('id').first()
        # repetition_count(scrape_object)
        if scrape_object:
            trending_object = Trending.objects.get(id=scrape_object.trending_id)
            short_content = generate_trend_topics(scrape_object.content, trending_object.topic)
            
            related_queries_rising = split_text(short_content, "Rising Related Queries", "Top Related Queries")
            related_queries_top = split_text(short_content, "Top Related Queries", "Rising Related Topics")
            related_topics_rising = split_text(short_content, "Rising Related Topics", "Top Related Topics")
            related_topics_top = split_text(short_content, "Top Related Topics", None)
            
            if related_queries_rising or related_queries_top or related_topics_rising or related_topics_top:
                data = {
                    'related_topics_rising' : json.dumps(related_topics_rising) if related_topics_rising != "null" else json.dumps([]),
                    'related_topics_top' : json.dumps(related_topics_top) if related_topics_top != "null" else json.dumps([]),
                    'related_query_rising' : json.dumps(related_queries_rising) if related_queries_rising != "null" else json.dumps([]),
                    'related_query_top' : json.dumps(related_queries_top) if related_queries_top != "null" else json.dumps([]),
                    'status' : 'Content Ready'}
                for key, value in data.items():
                    if hasattr(trending_object, key):
                        setattr(trending_object, key, value)
                trending_object.save()

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

    except Exception as e:
        logger.warning(f'Generate Related Trends Task Exception {e}')


@logger.catch
@shared_task
def generate_content_info_task():
    logger.warning("Generate Content Info Task Started")
    try:
        scrape_object = Scrape.objects.filter(status="Content Ready").order_by('id').first()
        # repetition_count(scrape_object)
        if scrape_object is None:
            logger.info("No 'Content Ready' scrape objects found.")
            return None
        print("id - ", scrape_object.id)
        print("trending_id - ", scrape_object.trending_id)
        short_content = json.loads(scrape_object.title) + json.loads(scrape_object.short_content)
        content = json.loads(scrape_object.title) + json.loads(scrape_object.content)
        print("check")
        generate_post_content_info = generate_content_info(short_content)
        print("kokokokok")
        if generate_post_content_info == "":
                scrape_object.status = "Blocked"
                scrape_object.save()
        else:
            category = split_text(generate_post_content_info, "Category", "Sub Category")
            subcategory = split_text(generate_post_content_info, "Sub Category", "Tags")
            tags = split_text(generate_post_content_info, "Tags", None)
            
            if Post.objects.filter(post_id=scrape_object.trending_id).exists():
                logger.warning("Post item already exists")
                scrape_object.status = "Joined"
            else:
                post_object = Post(
                    post_id=scrape_object.trending_id,
                    title="NoNE",
                    subtitle="NoNE",
                    meta="NoNE",
                    content=json.dumps(content),
                    conclusion="NoNE",
                    category=json.dumps(category),
                    subcategory=json.dumps(subcategory),
                    tags=json.dumps(tags),
                    author="NoNE",
                    status="Pre Content",
                    image_prompt="NoNE",
                    image_path="NoNE",
                    image_data="NoNE"
                )
                post_object.save()
                scrape_object.status = "Joined"
        
        scrape_object.save()
        logger.warning("Generate Content Info Task Ended")
        return None
    except Exception as e:
        logger.exception(f"Generate Content Info Task Exception: {e}")
        return None


@logger.catch
@shared_task
def generate_content_task():
    logger.warning("Generate Content Task Started")
    try:
        post_object = Post.objects.filter(status="Pre Content").order_by('id').first()
        # repetition_count(post_object)
        if not post_object:
            logger.warning("No post found with status 'Pre Content'")
            return

        topics_object = Trending.objects.get(id=post_object.post_id)
        scrape_object = Scrape.objects.get(trending_id=post_object.post_id)

        related_topic = json.loads(topics_object.related_topics_rising) + json.loads(topics_object.related_topics_top)
        related_query = json.loads(topics_object.related_query_rising) + json.loads(topics_object.related_query_top)
        
        content = json.loads(post_object.content)

        generate_post_content, author_name = generate_content(
            topics_object.topic,
            scrape_object.short_content,
            content,
            related_topic,
            related_query,
            json.loads(post_object.category)
        )
        if generate_post_content != "":
            questions_list = generate_content_cta(generate_post_content)

            cleaned_heading = split_text(generate_post_content, "Heading", "Introduction")
            cleaned_subheading = split_text(generate_post_content, "Introduction", "Body")
            cleaned_content = split_text(generate_post_content, "Body", "Conclusion")
            cleaned_conclusion = split_text(generate_post_content, "Conclusion", None)

            if not all([cleaned_heading, cleaned_subheading, cleaned_content, cleaned_conclusion]):
                data = {
                    'title': 'none',
                    'subtitle': 'none',
                    'content': 'none',
                    'conclusion': 'none',
                    'author': author_name,
                    'status': 'Content Issue'
                }
            else:
                data = {
                    'title': json.dumps(cleaned_heading),
                    'subtitle': json.dumps(cleaned_subheading),
                    'content': json.dumps(cleaned_content),
                    'conclusion': json.dumps(cleaned_conclusion),
                    'author': author_name,
                    'status': 'Post Content',
                    'survey': questions_list
                }
            for key, value in data.items():
                if hasattr(post_object, key):
                    setattr(post_object, key, value)
            post_object.save()
        else:
            post_object.status = "Blocked"
            post_object.save()
        logger.warning("Generate Content Task Ended")
    except Exception as e:
        logger.error(f'Generate Content Task Exception: {e}', exc_info=True)


@logger.catch
@shared_task
def generate_image_prompt_task():
    """
    Task to generate image prompts from post content and conclusion.

    This task finds the first Post object with status 'Post Content',
    generates an image prompt from its content and conclusion,
    updates the Post object with the generated image prompt and status,
    and saves the changes to the database.

    If an exception occurs, it is logged and the task exits gracefully.
    """
    logger.warning("Generate Image Prompt Task Started")
    try:
        post_object = Post.objects.filter(status="Post Content").order_by('id').first()
        # repetition_count(post_object)
        if post_object:
            image_prompt_content = (
                [item for item in json.loads(post_object.content)] +
                [item for item in json.loads(post_object.conclusion)]
            )
            image_prompt = generate_image_prompt(image_prompt_content)
            post_object.image_prompt = image_prompt
            post_object.status = 'ImageGenReady'
            post_object.save()
            logger.warning("Generate Image Prompt Task Completed")
        else:
            logger.info("No Post object with status 'Post Content' found.")
    except Exception as e:
        logger.error(f"Generate Image Prompt Task Exception: {e}")
        return None

@logger.catch
@shared_task
def generate_image_task():
    """Generate an image for a post with status 'ImageGenReady'."""
    logger.info("Generate Image Task Started")
    try:
        post_object = Post.objects.filter(status="ImageGenReady").order_by('id').first()
        post_object.status = "In Process"
        post_object.save()
        # repetition_count(post_object)
        if post_object:
            logger.info(f"Processing post with ID: {post_object.id}")

            crm_path, image_path, base64_image = asyncio.run(generate_image_api(post_object.image_prompt, post_object.id))

            image_data = [post_object.image_prompt, str(crm_path), str(image_path), base64_image]
            all_image_datas = [image_data]
            all_image_data = json.dumps(all_image_datas)

            data = {
                'image_crm': crm_path,
                'image_path': image_path,
                'all_image_data': all_image_data,
                'image_data': base64_image,
                'status': 'Meta Ready'
            }

            for key, value in data.items():
                if hasattr(post_object, key):
                    setattr(post_object, key, value)
            post_object.save()
            
            logger.info("Generate Image Task Ended")
        else:
            logger.warning("No post found with status 'ImageGenReady'")
    except Exception as e:
        logger.error(f"Generate Image Task Exception: {e}")


@logger.catch
@shared_task
def generate_meta_info_task():
    """Task to generate meta information for posts with status 'Meta Ready'."""
    logger.warning("Generate Meta Task Started")
    try:
        # Fetch the first post with status 'Meta Ready'
        post_object = Post.objects.filter(status="Meta Ready").order_by('id').first()
        # repetition_count(post_object)
        if post_object:
            # Fetch the related trending object
            trending_object = Trending.objects.get(id=post_object.post_id)

            # Parse
            # Combine related topics and queries
            related_topics = json.loads(trending_object.related_topics_rising) + json.loads(trending_object.related_topics_top)
            related_query = json.loads(trending_object.related_query_rising) + json.loads(trending_object.related_query_top)

            # Generate meta information
            meta = generate_meta_info(related_topics, related_query, post_object.content)

            # Update post object
            post_object.meta = meta
            post_object.status = 'Draft'
            post_object.save()
            
            logger.info(f"Meta information generated for post id {post_object.id}")
        
        logger.warning("Generate Meta Task Ended")
    except Post.DoesNotExist:
        logger.error("No post found with status 'Meta Ready'")
    except Trending.DoesNotExist:
        logger.error(f"Trending object with id {post_object.post_id} not found")
    except Exception as e:
        logger.exception(f'Generate Meta Task Exception: {e}')

@shared_task
def fetch_api_website():
    """
    Fetch data from the API and update the Post model in the database.

    Makes a GET request to the API endpoint, processes the response, and updates
    the Post model accordingly.
    """
    api_url = os.getenv('API_URL', 'http://tewsletter.com/api/postapi/saved/')
    logger.info("API hit Website Started")
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raises HTTPError for bad responses

        data = response.json()
        logger.info("API hit successful!")
        
        for item in data:
            post_id = item.get('post_id')
            if post_id is None:
                logger.warning("post_id is missing in the API response item")
                continue

            post_object = Post.objects.filter(post_id=post_id)
            if post_object: 
                post_object.status = "Sent"
                post_object.save()
                logger.info(f"Post {post_id} status updated to 'Sent'")
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
    except ValueError as e:
        logger.error(f"JSON decoding failed: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


################################## Regenrate Task Functions ####################################

@logger.catch
@shared_task
def regenerate_content_task(id):
    logger.warning("Regenerate Content Task Started")
    try:
        post_object = Post.objects.get(post_id = id)
        
        topics_object = Trending.objects.get(id= id)
        scrape_object = Scrape.objects.get(trending_id = id)
        
        logger.warning("Regenerate Content Task Working")

        related_topic = json.loads(topics_object.related_topics_rising) + json.loads(topics_object.related_topics_top)
        related_query = json.loads(topics_object.related_query_rising) + json.loads(topics_object.related_query_top)
        
        content = json.loads(post_object.content)

        generate_post_content, author_name = generate_content(
            topics_object.topic,
            scrape_object.short_content,
            content,
            related_topic,
            related_query,
            json.loads(post_object.category)
        )
        if generate_post_content != "":
            questions_list = generate_content_cta(generate_post_content)

            cleaned_heading = split_text(generate_post_content, "Heading", "Introduction")
            cleaned_subheading = split_text(generate_post_content, "Introduction", "Body")
            cleaned_content = split_text(generate_post_content, "Body", "Conclusion")
            cleaned_conclusion = split_text(generate_post_content, "Conclusion", None)

            if not all([cleaned_heading, cleaned_subheading, cleaned_content, cleaned_conclusion]):
                data = {
                    'title': 'none',
                    'subtitle': 'none',
                    'content': 'none',
                    'conclusion': 'none',
                    'author': author_name,
                    'status': 'Content Issue'
                }
            else:
                data = {
                    'title': json.dumps(cleaned_heading),
                    'subtitle': json.dumps(cleaned_subheading),
                    'content': json.dumps(cleaned_content),
                    'conclusion': json.dumps(cleaned_conclusion),
                    'author': author_name,
                    'status': 'Draft',
                    'survey': questions_list
                }
            for key, value in data.items():
                if hasattr(post_object, key):
                    setattr(post_object, key, value)
            post_object.save()
        else:
            post_object.status = "Blocked"
            post_object.save()
        logger.warning("Re Generate Content Task Ended")
        return None
    except Exception as e:
    #     # Handle any exceptions that may occur
        logger.warning(f'Regenerate Content Task Working {e}')

     
@logger.catch
@shared_task    
def regenerate_image_task(id):
    logger.warning("Regenerate Image Task Working")
    try:
        post_object = Post.objects.get(post_id=id)
        
        image_prompt_content = (
                [item for item in json.loads(post_object.content)] +
                [item for item in json.loads(post_object.conclusion)]
            )
        
        image_prompt = generate_image_prompt(image_prompt_content)
        post_object.image_prompt = image_prompt
                
        crm_path, image_path, base64_image = asyncio.run(generate_image_api(post_object.image_prompt, post_object.id))

        image_data = [post_object.image_prompt, str(crm_path), str(image_path), base64_image]
            
        all_image_datas = []
        
        all_image_datas = json.loads(post_object.all_image_data)
        all_image_datas.append(image_data)
        all_image_data = json.dumps(all_image_datas)
        

        data = {'image_crm' : crm_path, 'image_path' : image_path, 'all_image_data' : all_image_data, 'image_data' : base64_image,'status' : 'Draft'}

        for key, value in data.items():
            if hasattr(post_object, key):
                setattr(post_object, key, value)
        post_object.save()
        logger.warning("Regenerate Image Task Ended")
    except Exception as e:
    #     # Handle any exceptions that may occur
        logger.warning(f'Regenerate Image Task Exception {e}')

################################## Functions ####################################

# def repetition_count(object):
#     rep = int(object.rep_count)
#     if rep > 3:
#         object.status = "Blocked"
#     else:
#         rep = rep + 1
#         object.rep_count = rep
#     object.save()

##################################  Twitter Post Functions ####################################

@logger.catch
@shared_task
def generate_twitter_post_task():
    try:
        post_object = Post.objects.filter(status="Twitter Ready").order_by('id').first()
        if post_object:
            tweet_content = generate_twitter_post(post_object.conclusion)
            logger.warning(f'Generated Twitter post content: {tweet_content}')
            tweet_content_list = split_text(tweet_content, "Tweet", None)
            logger.warning(f'Split Twitter post content: {tweet_content_list}' )

            twitter_object = TwitterPost(
                post_id=post_object.id,
                content=json.dumps(tweet_content_list),
                status="Tweet Saved"
            )
            twitter_object.save()
            logger.warning("TwitterPost table updated")

            post_object.status = "Draft"
            post_object.save()
            logger.warning("Post table updated")
    except Exception as e:
        logger.warning(f'Exception in generate_twitter_post_task: {e}')

@logger.catch
@shared_task
def publish_twitter_post_task():
    try:
        twitter_object = TwitterPost.objects.filter(status="Tweet Saved").order_by('id').first()
        if twitter_object:
            twitter_client = get_twitter_client()
            tweet_content = json.loads(twitter_object.content)

            for tweet in tweet_content:
                twitter_client.create_tweet(text=tweet)

            twitter_object.status = "Tweet Published"
            twitter_object.save()
            logger.warning("TwitterPost table updated")
        
    except Exception as e:
        logger.warning(f'Exception in publish_twitter_post_task: {e}')
