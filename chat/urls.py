from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Login, name='Login'),

    path('logout/', views.Logout, name='Logout'),   
    
    path('chatbot/', views.chatbot, name='chatbot'),
    path('process_user_input/', views.process_user_input, name='process_user_input'),
    path('fetch_response_by_task_id/<str:task_id>/', views.fetch_response_by_task_id, name='fetch_response_by_task_id'),
    path('fetch_all_messages/', views.fetch_all_messages, name='fetch_all_messages'),
]