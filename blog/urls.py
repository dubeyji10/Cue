from django.urls import path
from .views import PostListView,PostDetailView,PostCreateView,PostUpdateView,PostDeleteView,UserPostListView,PostMonthArchiveView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

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
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('search/',views.post_search,name="post_search"),  
    #add path for /accounts  
    path('user/<str:username>',UserPostListView.as_view(),name='user-posts'),
    path('archive/<int:year>/month/<int:month>', PostMonthArchiveView.as_view(month_format='%m'), name='blog_archive_month'),
]


if settings.DEBUG:
    urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)