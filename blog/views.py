from django.shortcuts import render,redirect,render_to_response
from .models import Post,Comment
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
#added on 19nov
#----------------------------------------------------------------------------
#imported TemplateView

# class SearchView(TemplateView):
#     try:
#         template_name = 'blog/search.html'
#         def get(self, request, *args, **kwargs):
#             q = request.GET.get('q', '')
#         #self.results= Post.objects.filter(Q(title__icontains='q'))
#             results = []
#             results = Post.objects.filter(title__icontains=q).values
#             self.results=results
#             return super().get(request, *args, **kwargs)
        
#         def get_context_data(self, **kwargs):
#             return super().get_context_data(results=self.results, **kwargs)
#     except (ObjectDoesNotExist, MultipleObjectsReturned):
#         pass
    


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


def announcemnet(request):
    return render(request,'blog/announcemnet.html',{'title': 'Announcement'})

def welcome(request):
    return render(request,'blog/welcome.html',{'title':'Welcome'})


# def search(request):
#     query_string = ''
#     found_entries = None
#     if ('q' in request.GET) and request.GET['q'].strip():
#         query_string = request.GET['q']
#         entry_query = utils.get_query(query_string, ['title', 'body',])
#         posts = Post.objects.filter(entry_query).order_by('created')
#         return render(request, 'blog/search.html', { 'query_string': query_string, 'posts': posts })
#     else:
#         return render(request, 'blog/search.html', { 'query_string': 'Null', 'found_entries': 'Enter a search term' })


# def search(request):
#     query_string = ''
#     found_entries = None
#     if ('q' in request.GET) and request.GET['q'].strip():
#         query_string = request.GET['q']

#         entry_query = get_query(query_string, ['title', 'content',])

#         found_entries = Entry.objects.filter(entry_query).order_by('-date_posted')

#     return render_to_response('blog/search_results.html',
#                           { 'query_string': query_string, 'found_entries': found_entries },
#                           context_instance=RequestContext(request))

# def search(request):
#     query=None
#     context=None
#     results=None
#     trigram_results=None
#     result=None
#     form=SearchForm()
#     if 'query' in request.GET:
#         form=SearchForm(request.GET)
#         if form.is_valid():
#             query=form.cleaned_data['query']
#             print(query)
#             search_vector = SearchVector('title', 'body')
#             search_query = SearchQuery(query)
#             result=Post(search=search_vector,rank=SearchRank(search_vector,search_query)).filter(search=search_query).order_by('-rank')
#             trigram_results=Post.published.annotate(similarity=TrigramSimilarity('title',query)).filter(similarity__gt=0.3).order_by('-similarity')
#     context={'form':form,'results':trigram_results,'result':result,'query':query}
#     template='blog/search.html'
#     return render(request,template,context)

#
# #
# Handle 404 Errors
# @param request WSGIRequest list with all HTTP Request
# def error404(request,exception):

#     # 1. Load models for this view
#     #from idgsupply.models import My404Method

#     # 2. Generate Content for this view
#     template = loader.get_template('blog/error_404.html')
#     context = Context({
#         'message': 'All: %s' % request,
#         })

#     # 3. Return Template for this view + Data
#     return HttpResponse(content=template.render(context), content_type='text/html; charset=utf-8', status=404)

# def notfound(request, exception):
#     return render(request,'blog/error_404.html')
#

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

