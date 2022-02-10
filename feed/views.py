from statistics import mode
from django.shortcuts import render
from django.views.generic import DetailView,TemplateView,ListView,UpdateView,DeleteView
from django.views.generic.edit import CreateView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from followers.models import Follower
from .forms import PostForm

# Create your views here.
class HomePageVeiw(TemplateView):
    http_method_names = ["get"]
    template_name = 'feed/index.html'
    
    def dispatch(self, request, *args,**kwargs) :
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self,*args,**kwargs):

        context = super().get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:
            follwing = list(Follower.objects.filter(followed_by=self.request.user).values_list("following",flat=True))
            posts = Post.objects.filter(author__in=follwing).order_by('-id')
            if not posts:
                posts = Post.objects.all().order_by('-id')
        else:    
            posts = Post.objects.all().order_by('-id')
        context['posts'] = posts    
        return context

class AllPostsView(LoginRequiredMixin,ListView):
    http_method_names = ["get"]
    template_name = 'feed/all_posts.html'
    model = Post
    ordering = '-id' 
    context_object_name = "posts"


class MyPostsView(LoginRequiredMixin,ListView):
    http_method_names = ['get']
    template_name = 'feed/all_posts.html'
    model = Post

    def dispatch(self, request, *args,**kwargs) :
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self,*args,**kwargs):

        context = super().get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:
            posts = Post.objects.filter(author=self.request.user).order_by('-id')
        context['posts'] = posts    
        return context

class PostDetailView(DetailView):
    http_method_names = ["get"]
    template_name = 'feed/detail.html'
    model = Post
    context_object_name = "post"


class CreateNewPost(LoginRequiredMixin, CreateView):

    template_name="feed/newpost.html"
    model = Post
    fields = ["text"]
    success_url = '/'

    def dispatch(self, request, *args,**kwargs) :
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self,form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super().form_valid(form)

    def post(self,request, *args, **kwargs):
        post = Post.objects.create(
                text = request.POST.get("text"), 
                author= request.user )
        return render(
            request,
            "includes/post.html",
            {
                "post":post,
                "showdetail":True
            },
            content_type="application/html"
        )

class UpdatePostView(LoginRequiredMixin,UpdateView):
    template_name="feed/newpost.html"
    model = Post
    form_class = PostForm
    success_url = '/my_posts'

class DeletePostView(LoginRequiredMixin, DeleteView):
    template_name = 'feed/delete.html'
    model = Post
    success_url = '/my_posts'    




  
            
