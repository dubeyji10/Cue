from django.urls import path
from .views import PostListView,PostDetailView,PostCreateView,PostUpdateView,PostDeleteView,UserPostListView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.generic.dates import ArchiveIndexView
from .models import Post
urlpatterns = [

    path('',views.welcome,name='cue'),#remove this line just checking something
    path('home/',PostListView.as_view(),name='blog-home'),#homepage now
                 #calls home function
    path('about/',views.about,name='blog-about'),#.../about
             #call about function
    path('announcemnet/',views.announcemnet,name='blog-announcemnet'),#another simple page
    path('post/<int:pk>/',PostDetailView.as_view(),name = 'post-detail'),
            #pk - primary key int-integer type
    path('post/new/',PostCreateView.as_view(),name = 'post-create'),
    path('post/<int:pk>/update',PostUpdateView.as_view(),name = 'post-update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name = 'post-delete'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    #path('search/',views.searchposts,name="post_search"),  
    #add path for /accounts  
    path('user/<str:username>',UserPostListView.as_view(),name='user-posts'),
    #path('archive/<int:year>/month/<int:month>', PostMonthArchiveView.as_view(month_format='%m'), name='post_archive_month'),
    #path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    path('archive/',ArchiveIndexView.as_view(model=Post, date_field="date_posted"),name="archives"),
    path('latest_posts/',views.latest_posts,name='latest-posts'),
    #path('search/', SearchResultsView.as_view(), name='search_results'),

]


if settings.DEBUG:
    urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)