from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view
from crm.models import Scrape, Post, Trending
from django.http import JsonResponse
from crm.tasks import regenerate_content_task, regenerate_image_task, fetch_trends_realtime_task
import requests
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
        
    }
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
def view_scrape(request):
    #View function for rendering scraped posts.
    id_value = request.GET.get('id')
    all_scraped = Scrape.objects.get(id=id_value)
    
    context = {'title': 'Scrape', 'success': "this is success", 'all_scraped': all_scraped}
    return render(request, "dashboard/viewscrape.html", context)

@csrf_exempt
def view_post(request):
    #View function for rendering scraped posts.
    id_value = request.GET.get('id')
    all_posts = Post.objects.get(id=id_value)
    # print("--------all scraped ----------",all_scraped, id_value)
    context = {'title': 'Posts', 'success': "this is success", 'all_posts': all_posts}
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
        id_value = request.POST.get('value')
        print(id_value,"id76767676")
        regenerate_image_task.apply_async(args=[id_value])
        all_posts = Post.objects.get(post_id=id_value)
        context = {'title': 'Index', 'success': "this is success", 'all_posts': all_posts}
    return render(request, "dashboard/viewpost.html", context)

@csrf_exempt
def trend(request):
    with open('logs/testing.log', 'r') as file:
        log_data = file.read()

    # Pass log data to template
    return render(request, 'dashboard/viewlogs.html', {'log_data': log_data})
#     fetch_trends_realtime_task.apply_async()
    # return render(request, "dashboard/index.html")

@csrf_exempt
def previous_post(request):
    if request.method == 'POST':
        id_value = request.POST.get('value')
        all_posts = Post.objects.get(post_id = id_value)
        id_value = int(all_posts.id)
        id_value = id_value + 1
        all_posts = Post.objects.get(id = id_value)
        context = {'title': 'Posts', 'success': "this is success", 'all_posts': all_posts}
    return render(request, "dashboard/viewpost.html", context)

@csrf_exempt
def next_post(request):
    if request.method == 'POST':
        id_value = request.POST.get('value')
        all_posts = Post.objects.get(post_id = id_value)
        id_value = int(all_posts.id)
        id_value = id_value + 1
        all_posts = Post.objects.get(id = id_value)
        context = {'title': 'Posts', 'success': "this is success", 'all_posts': all_posts}
    return render(request, "dashboard/viewpost.html", context)

@csrf_exempt
def toggle_task(request):
    if request.method == 'POST':
        task_name = request.POST.get('value')
        try:
            task = PeriodicTask.objects.get(name=task_name)
            task.enabled = not task.enabled
            task.save()
            return JsonResponse({'status': 'success', 'message': f'Task {"resumed" if task.enabled else "paused"} successfully.', 'enabled': task.enabled})
        except PeriodicTask.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Task does not exist.'})
