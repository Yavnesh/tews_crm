from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view
from crm.models import Scrape, Post, Trending
from django.http import JsonResponse
from crm.tasks import regenerate_content_task, regenerate_image_task, fetch_trends_realtime_task
import requests
# Create your views here.
@csrf_exempt
def crm_dashboard(request):
    # View function for rendering CRM dashboard.
    context = {'title': 'Index', 'success': "this is success"}
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
    fetch_trends_realtime_task.apply_async()
    return render(request, "dashboard/index.html")

