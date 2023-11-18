from django.urls import path
from . import views
urlpatterns = [
    path('',views.get_routes,name='routes'),
    path('rooms/',views.get_rooms,name='rooms'),
    path('room/<int:pk>/',views.get_room,name='room'),
    
]