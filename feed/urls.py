from django.urls import path
from . import views
from feed.models import Post
from .views import HomePageVeiw,PostDetailView, CreateNewPost,AllPostsView,MyPostsView,UpdatePostView,DeletePostView

app_name='feed'


urlpatterns = [
    path('', views.HomePageVeiw.as_view() , name="home"),
    path('all_posts/', views.AllPostsView.as_view() , name="all_posts"),
    path('my_posts/', views.MyPostsView.as_view() , name="my_posts"),
    path('detail/<int:pk>/', views.PostDetailView.as_view() , name="detail"),
    path('new/', views.CreateNewPost.as_view() , name="newpost"),
    path('update/<int:pk>', views.UpdatePostView.as_view() , name="update-post"),
    path('delete/<int:pk>', views.DeletePostView.as_view() , name="delete-post"),


]