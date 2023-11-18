from django.urls import path
from . import views
urlpatterns=[
    path('login/' , views.login_page , name='login'),
    path('register_page' , views.register_page , name='register'),
    path('logout/' , views.logout_user , name='logout'),
    path('' , views.home , name='home'),
    path('room/<str:pk>/' , views.room , name='room'),
    path('profile/<str:pk>/' , views.user_profile , name='profile'),
    path('update-user/<str:pk>/' , views.update_user , name='update_user'),
    path('create_room/' , views.create_room , name='create_room'),
    path('update_room/<str:pk>/' , views.update_room , name='update_room'),
    path('delete_room/<str:pk>/' , views.delete_room , name='delete_room'),
    path('delete_message/<str:pk>/' , views.delete_message , name='delete_message'),
    path('topics/' , views.topic_page , name='topics'),
    path('activity/' , views.activities_page , name='activity'),

]