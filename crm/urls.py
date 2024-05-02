from django.urls import path
# from django.conf import settings
# from django.conf.urls.static import static
from crm import views
# from crm.tasks import clear_cache

urlpatterns = [
    path('', views.crm_dashboard, name='crm_dashboard'),
    path('topics/', views.topics, name='topics'),
    path('view_topics/', views.view_topics, name='view_topics'),
    path('view_scrape/', views.view_scrape, name='view_scrape'),
    path('view_post/', views.view_post, name='view_post'),
    # path('regenerate_info/', views.regenerate_info, name='regenerate_info'),
    # path('regenerate_content/', views.regenerate_content, name='regenerate_content'),
    # path('regenerate_image_prompt/', views.regenerate_image_prompt, name='regenerate_image_prompt'),
    # path('regenerate_image/', views.regenerate_image, name='regenerate_image'),
    path('scrape/', views.scrape, name='scrape'),
    path('posts/', views.posts, name='posts'),
    # path('create-post/', views.create_post, name='create_post'),
    # path('create-image/', views.create_image, name='create_image'),

    # path('post/', views.post_detail, name='post_detail'),
    # path('gtrends/', views.gtrends, name='gtrends'),
    # url(r'^student/dashboard/$', views.dashboard, name='Dashboard'),
    # url(r'^student/classroom/$', views.classroom, name='Classroom'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)