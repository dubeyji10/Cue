from django.shortcuts import render,redirect
from .models import Post,Comment
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from PIL import Image
from .forms import CommentForm,SearchForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Permission, User
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.views.generic.dates import YearArchiveView,MonthArchiveView

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
class PostYearArchiveView(YearArchiveView):
    queryset = Post.objects.all()
    date_field = "date_posted"
    make_object_list = True
    allow_future = True
   
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


def about(request):
    return render(request,'blog/about.html',{'title': 'About Blog'})

def welcome(request):
    return render(request,'blog/welcome.html',{'title':'Welcome'})

def post_search(request):
    query=None
    context=None
    results=None
    trigram_results=None
    result=None
    form=SearchForm()
    if 'query' in request.GET:
        form=SearchForm(request.GET)
        if form.is_valid():
            query=form.cleaned_data['query']
            print(query)
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            result=Post.published.annotate(search=search_vector,rank=SearchRank(search_vector,search_query)).filter(search=search_query).order_by('-rank')
            trigram_results=Post.published.annotate(similarity=TrigramSimilarity('title',query)).filter(similarity__gt=0.3).order_by('-similarity')
    context={'form':form,'results':trigram_results,'result':result,'query':query}
    template='blog/search.html'
    return render(request,template,context)