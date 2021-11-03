from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),

    path('room/<str:pk>/', views.room, name='room'),
    path('create-room/', views.createRoom, name='create_room'),
    path('update-room/<str:pk>/', views.updateRoom, name='update_room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete_room'),

    path('profile/<str:pk>/', views.userProfile, name='profile'),
    
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('update-user/', views.updateUser, name='update_user'),

    path('delete-message/<str:pk>/<str:rpk>/', views.deleteMessage, name='delete_message'),

    path('topics/', views.topicsPage, name='topics'),
    path('activitys/', views.activitysPage, name='activitys'),
]