from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('channels/',views.podchannels,name='podchannels'),
    path('login/',views.userlogin,name='userlogin'),
    path('logout/',views.userlogout,name='userlogout'),
    path('signup/',views.signup,name='signup'),
    path('stream/<str:room_name>/', views.podstream, name='podstream'),
    path('stream/<str:room_name>/<str:audio_name>/', views.podstreamredirect, name='podstreamredirect'),
    path('studio/<str:user_name>/', views.podstudio, name='podstudio'),
    path('studio/<str:user_name>/', views.podstudio, name='podstudio'),
]