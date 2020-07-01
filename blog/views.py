from django.shortcuts import render,redirect
from .models import Post,Comment,Like
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from PIL import Image
from .forms import CommentForm,SearchForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Permission, User
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.views.generic.dates import YearArchiveView,MonthArchiveView,WeekArchiveView
from django.template import loader,Context
from django.http import HttpResponse
from datetime import *
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def home(request):
    context = {
        'posts':Post.objects.all()
    }
    return render(request,'blog/home.html',context)

    
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4


class PostDetailView(DetailView):
    model = Post

#adding month view
# class PostMonthArchiveView(MonthArchiveView):
#     queryset = Post.objects.all()
#     date_field = "date_posted"
#     allow_future = True

# def archive(request, year, month):
#     post_list = Post.objects.filter(date_posted__year=year,date_posted__month=month).order_by('-date_posted')
#     return render(request, 'blog/index.html', context={'post_list': post_list})

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    #ordering = ['-date_posted']
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
        
class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content','image']#remove image

    def form_valid(self,form):
        #setting the author to the logged in
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title','content','image']

    def form_valid(self,form):#setting the author to the logged in
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False #403 -forbidden 

class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/home'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False #403 -forbidden 


class SearchView(ListView):
    model = Post
    template_name = 'blog/search.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
       result = super(SearchView, self).get_queryset()
       query = self.request.GET.get('q')
       if query:
          postresult = Post.objects.filter(title__contains=query)
          result = postresult
       else:
           result = None
       return result


#
# class SearchView(TemplateView):
#     template_name = 'blog/search.html'
#     model = Post
#     def get_queryset(self):
#         query = self.request.GET.get('q')
#         object_list= Post.objects.filter(Q(title__icontains='q'))
#         return object_list

#----------------------------------------------------------------------------
@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post-detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post-detail', pk=comment.post.pk)
#---------- 7July 2020-------------------
@login_required()
def like(request,pk):
    requested_post = Post.objects.get(id = pk)
    current_user = request.user
    if_voted = Like.objects.filter(post = requested_post,user = current_user).count()
    unlike_parameter = Like.objects.filter(post = requested_post,user = current_user)

    if if_voted==0:
        requested_post.likes +=1
        requested_post.save()
        like = Like(user = current_user, post = requested_post )
        like.save_like()
        return redirect('post-detail', pk=pk)

    else:
        requested_post.likes -=1
        requested_post.save()
        for single_unlike in unlike_parameter:
            single_unlike.unlike()
        return redirect('post-detail', pk=pk)

    return render(request,'post-detail')



#
# @login_required
# def likes(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#
#     return redirect('post-detail', pk=likes.post.pk)
# ------------------------------
# return redirect()

def about(request):
    return render(request,'blog/about.html',{'title': 'About Blog'})


def announcemnet(request):
    return render(request,'blog/announcemnet.html',{'title': 'Announcement'})

def welcome(request):
    return render(request,'blog/welcome.html',{'title':'Welcome'})


def error_404_view(request, exception):
    data = {"name": "Cue"}
    return render(request,'blog/error_404.html', data)


def latest_posts(request):
    latest_posts = Post.objects.all()
    #page = request.GET.get('page')
    forms = Post.objects.filter(date_posted__lte=timezone.now()).order_by('-date_posted')[0:3]
    #paginator = Paginator(post_list, per_page=3)
    return render(request, 'blog/latest_posts.html', {'posts': latest_posts,'forms': forms,})


# def searchform(request):
#     return render(request, 'blog/search_form2.html')

def listallusers(request):
    all_users = User.objects.all()
    #page = request.GET.get('page')
    #forms = Post.objects.filter(date_posted__lte=timezone.now()).order_by('-date_posted')[0:3]
    #paginator = Paginator(post_list, per_page=3)
    return render(request, 'blog/AllUsers.html', {'all_users': all_users,})


# on July 7
# def submission(request, pk):
#     submission = get_object_or_404(Post, pk=int(pk))
#     pk = int(pk)
#
#     return render('')
    # return render_to_response('post.html',
    #                           {'submission':submission},
    #                           context_instance=RequestContext(request))