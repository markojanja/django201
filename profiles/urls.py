
from django.urls import path
from . import views
from .views import ProfileView,FollowView,UpdateProfileVeiw


app_name ="profiles"

urlpatterns = [
    path("<str:username>/", views.ProfileView.as_view(), name="detail"),
    path("<str:username>/follow/", views.FollowView.as_view(), name="follow"),
    path("<str:username>/update/", views.UpdateProfileVeiw.as_view(), name="update"),

    
]