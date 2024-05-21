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
    path('regenerate_content/', views.regenerate_content, name='regenerate_content'),
    path('trend/', views.trend, name='trend'),
    path('regenerate_image/', views.regenerate_image, name='regenerate_image'),
    path('scrape/', views.scrape, name='scrape'),
    path('posts/', views.posts, name='posts'),
    # path('previous_post/', views.previous_post, name='previous_post'),
    path('save_topics/', views.save_topics, name='save_topics'),

    path('toggle_task/', views.toggle_task, name='toggle_task'),
    path('add_topics/', views.add_topics, name='add_topics'),
    # url(r'^student/dashboard/$', views.dashboard, name='Dashboard'),
    # url(r'^student/classroom/$', views.classroom, name='Classroom'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)