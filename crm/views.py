from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view
from crm.models import Scrape, Post, Trending
from django.http import JsonResponse
from crm.tasks import regenerate_content_task, regenerate_image_task, fetch_trends_realtime_task
import requests, json
from django_celery_beat.models import PeriodicTask
##############  Loguru  #######################
from loguru import logger
logger.add("logs/file_Views_{time}.log",level="TRACE", rotation="10 MB")
# Create your views here.
@csrf_exempt
def crm_dashboard(request):
    # View function for rendering CRM dashboard.

    # draft_posts_count = Post.objects.filter(status='Draft').count()
    trending_details = {
        'total': Trending.objects.all().count(),

        'daily_total': Trending.objects.filter(source='Daily Trends').count(),
        'daily_blocked': Trending.objects.filter(source='Daily Trends', status='Blocked').count(),
        'daily_ready': Trending.objects.filter(source='Daily Trends', status='Content Ready').count(),
        'daily_scraped': Trending.objects.filter(source='Daily Trends', status='Scraped').count(),
        'daily_saved': Trending.objects.filter(source='Daily Trends', status='Saved').count(),

        'realtime_total': Trending.objects.filter(source='Real Time Trends').count(),
        'realtime_blocked': Trending.objects.filter(source='Real Time Trends', status='Blocked').count(),
        'realtime_ready': Trending.objects.filter(source='Real Time Trends', status='Content Ready').count(),
        'realtime_scraped': Trending.objects.filter(source='Real Time Trends', status='Scraped').count(),
        'realtime_saved': Trending.objects.filter(source='Real Time Trends', status='Saved').count(),


        'manual_total': Trending.objects.filter(source='Manual Trends').count(),
        'manual_blocked': Trending.objects.filter(source='Manual Trends', status='Blocked').count(),
        'manual_ready': Trending.objects.filter(source='Manual Trends', status='Content Ready').count(),
        'manual_scraped': Trending.objects.filter(source='Manual Trends', status='Scraped').count(),
        'manual_saved': Trending.objects.filter(source='Manual Trends', status='Saved').count(),
    }
    scrape_details = {
        'total': Scrape.objects.all().count(),
        'trends_ready': Scrape.objects.filter(status='Trends Ready').count(),
        'blocked': Scrape.objects.filter(status='Blocked').count(),
        'content_ready': Scrape.objects.filter(status='Content Ready').count(),
        'scrape': Scrape.objects.filter(status='Scraped').count(),
        'joined': Scrape.objects.filter(status='Joined').count(),
    }
    post_details = {
        'total': Post.objects.all().count(),
        'pre_content': Post.objects.filter(status='Pre Content').count(),
        'content_issue': Post.objects.filter(status='Content Issue').count(),
        'post_content': Post.objects.filter(status='Post Content').count(),
        'image_gen_ready': Post.objects.filter(status='ImageGenReady').count(),
        'image_in_process': Post.objects.filter(status='In Process').count(),
        'meta_ready': Post.objects.filter(status='Meta Ready').count(),
        'draft': Post.objects.filter(status='Draft').count(),
        'sent': Post.objects.filter(status='Sent').count(),
        'blocked': Post.objects.filter(status='Blocked').count(),
        
    }
    task_object = {
        'generate_short_content_task_periodic': PeriodicTask.objects.get(name='generate_short_content_task_periodic').enabled,
        'generate_realated_trend_task_periodic': PeriodicTask.objects.get(name='generate_realated_trend_task_periodic').enabled,
        'generate_content_info_task_periodic': PeriodicTask.objects.get(name='generate_content_info_task_periodic').enabled,
        'generate_content_task_periodic': PeriodicTask.objects.get(name='generate_content_task_periodic').enabled,
        'generate_meta_info_task_periodic': PeriodicTask.objects.get(name='generate_meta_info_task_periodic').enabled,
        'generate_image_prompt_task_periodic': PeriodicTask.objects.get(name='generate_image_prompt_task_periodic').enabled,
        'fetch_api_website_task_periodic': PeriodicTask.objects.get(name='fetch_api_website_task_periodic').enabled,
        'generate_image_task_periodic': PeriodicTask.objects.get(name='generate_image_task_periodic').enabled,
        'fetch_trends_task_periodic': PeriodicTask.objects.get(name='fetch_trends_task_periodic').enabled,
        'fetch_trends_realtime_task_periodic': PeriodicTask.objects.get(name='fetch_trends_realtime_task_periodic').enabled,
        'fetch_article_data_task_periodic': PeriodicTask.objects.get(name='fetch_article_data_task_periodic').enabled,
        'turn_off_all': PeriodicTask.objects.get(name='celery.backend_cleanup').enabled,
    }
    # PeriodicTask.objects.get(name='fetch_trends_realtime_task_periodic').enabled = False
    # trending_topic_count = Trending.objects.filter(status='Draft').count()
    context = {'title': 'Index', 'success': "this is success", 'task_object': task_object, 'post_details': post_details, 'scrape_details': scrape_details, 'trending_details': trending_details,}
    logger.warning("THis is jaust a check ")
    return render(request, "dashboard/index.html", context)

@csrf_exempt
def view_topics(request):
    #View function for rendering scraped posts.
    id_value = request.GET.get('id')
    all_trending = Trending.objects.get(id=id_value)
    
    context = {'title': 'Topic', 'success': "this is success", 'all_trending': all_trending}
    return render(request, "dashboard/viewtopic.html", context)

@csrf_exempt
def add_topics(request):
    context = {'title': 'Topic', 'success': "this is success"}
    return render(request, "dashboard/add_topics.html", context)

@csrf_exempt
def save_topics(request):
    if request.method == 'POST':
        topics_input = request.POST.get('value')
        try:
            topics_list = eval(topics_input)  # Convert string representation of list to actual list
            if isinstance(topics_list, list):
                for topic_name in topics_list:
                    if not Trending.objects.filter(topic=topic_name):
                        Trending.objects.create(topic=topic_name,status="Saved",source="Manual Trends")
            context = {'title': 'Topic', 'success': 'this is success'}
            return JsonResponse(context)
              # Redirect to a success page or another view
        except (SyntaxError, ValueError):
            # Handle the case where eval fails to parse the input correctly
            pass

@csrf_exempt
def view_scrape(request):
    #View function for rendering scraped posts.
    id_value = request.GET.get('id')
    all_scraped = Scrape.objects.get(id=id_value)
    
    context = {'title': 'Scrape', 'success': "this is success", 'all_scraped': all_scraped}
    return render(request, "dashboard/viewscrape.html", context)

@csrf_exempt
def view_post(request):
    #View function for rendering scraped posts.
    first_post = Post.objects.all().order_by('id').first()
    last_post = Post.objects.all().order_by('-id').first()
    id_value = request.GET.get('id')
    if id_value==None:
        id_value = last_post.id
    if str(first_post.id) == str(id_value):
        previous_post = Post.objects.all().order_by('-id').first()
    else:
        previous_post = Post.objects.filter(id__lt=id_value).order_by('-id').first()
    if str(last_post.id) == str(id_value):
        next_post = Post.objects.all().order_by('id').first()
    else:
        next_post = Post.objects.filter(id__gt=id_value).order_by('id').first()
    all_posts = Post.objects.get(id=id_value)
    all_images = json.loads(Post.objects.get(id=id_value).image_crm)
    previous_id = previous_post.id
    next_id = next_post.id
    
    # print("--------all scraped ----------",all_scraped, id_value)
    context = {'title': 'Posts', 'success': "this is success", 'all_images': all_images, 'all_posts': all_posts, 'previous_id': previous_id, 'next_id': next_id}
    return render(request, "dashboard/viewpost.html", context)

@csrf_exempt
def topics(request):
    #View function for rendering URL page.
    all_trending = Trending.objects.all()
    context = {'title': 'Topic',"all_trending": all_trending}
    return render(request, "dashboard/topic.html", context)

@csrf_exempt
def scrape(request):
    #View function for rendering URL page.
    all_scraped = Scrape.objects.all()
    context = {'title': 'Scrape',"all_scraped": all_scraped}
    return render(request, "dashboard/scrape.html", context)

@csrf_exempt
def posts(request):
    #View function for rendering URL page.
    all_posts = Post.objects.all()
    context = {'title': 'Posts',"all_posts": all_posts}
    return render(request, "dashboard/post.html", context)


@csrf_exempt
def regenerate_content(request):
    if request.method == 'POST':
        id_value = request.POST.get('value')  
        regenerate_content_task.apply_async(args=[id_value])
        all_posts = Post.objects.get(post_id=id_value)
        context = {'title': 'Index', 'success': "this is success", 'all_posts': all_posts}
        return render(request, "dashboard/viewpost.html", context)

@csrf_exempt
def regenerate_image(request):
    if request.method == 'POST':
        count = request.POST.get('id')
        id_value = request.POST.get('value')
        print(count,id_value)
        print(id_value,"id76767676")
        all_posts = Post.objects.get(id=count)
        regenerate_image_task(count, id_value)
        # regenerate_image_task.apply_async(args=[count, id_value])
        
    #     context = {'title': 'Index', 'success': "this is success", 'all_posts': all_posts, 'id' : count}
    # return JsonResponse({'title': 'Index', 'success': "this is success", 'all_posts': all_posts, 'id' : count})

@csrf_exempt
def trend(request):
    with open('logs/testing.log', 'r') as file:
        log_data = file.read()

    # Pass log data to template
    return render(request, 'dashboard/viewlogs.html', {'log_data': log_data})
#     fetch_trends_realtime_task.apply_async()
    # return render(request, "dashboard/index.html")

@csrf_exempt
def toggle_task(request):
    if request.method == 'POST':
        task_name = request.POST.get('value')
        try:
            if task_name == "turn_off_all":
                task = PeriodicTask.objects.get(name="celery.backend_cleanup")
                if task.enabled == False:
                    tasks = PeriodicTask.objects.all()
                    for item in tasks:
                        item.enabled = True
                        item.save()
                else:
                    tasks = PeriodicTask.objects.all()
                    for item in tasks:
                        item.enabled = False
                        item.save()
                return JsonResponse({'status': 'success', 'message': f'All Tasks {"resumed" if task.enabled else "paused"} successfully.', 'enabled': task.enabled})
            else:
                task = PeriodicTask.objects.get(name=task_name)
                task.enabled = not task.enabled
                task.save()
                return JsonResponse({'status': 'success', 'message': f'Task {"resumed" if task.enabled else "paused"} successfully.', 'enabled': task.enabled})
        except PeriodicTask.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Task does not exist.'})
