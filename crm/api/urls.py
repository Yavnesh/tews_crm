from django.urls import path
from crm.api import views

urlpatterns = [
    path('postapi/', views.PostAPI.as_view()),
    path('postapi/<int:pk>/', views.PostAPI.as_view()),
    
]