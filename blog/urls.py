from django.urls import path
from .views import PostListView,PostDetailView,PostCreateView,PostUpdateView,PostDeleteView
from . import views
urlpatterns = [
    path('',views.welcome,name='cue'),#remove this line just checking something
    path('home/',PostListView.as_view(),name='blog-home'),#homepage now
                 #calls home function
    path('about/',views.about,name='blog-about'),#.../about
             #call about function
    path('post/<int:pk>/',PostDetailView.as_view(),name = 'post-detail'),
            #pk - primary key int-integer type
    path('post/new/',PostCreateView.as_view(),name = 'post-create'),
    path('post/<int:pk>/update',PostUpdateView.as_view(),name = 'post-update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name = 'post-delete'),
    
    
]