from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='blog-home'),#homepage now
                 #calls home function
    path('about/',views.about,name='blog-about'),#.../about
             #call about function
]