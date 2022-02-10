from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.views import View
from django.views.generic import DetailView,View,TemplateView
from feed.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from followers.models import Follower
from .models import User
from .forms import UserUpdateForm,ProfileUpdateForm
from django.urls import  reverse_lazy





# Create your views here.
app_name = "profiles"

class ProfileView(DetailView):

    http_methods = ["GET"]
    template_name = "profiles/detail.html"
    model = User
    context_object_name = "user"  
    slug_field = "username"
    slug_url_kwarg = "username"


    def dispatch(self, request, *args , **kwargs):
        self.request =request

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        user = self.get_object()
        context = super().get_context_data(**kwargs)
        context['total_posts'] = Post.objects.filter(author=user).count()
        context['total_followers'] = Follower.objects.filter(following=user).count()
        if self.request.user.is_authenticated:
            context["u_follow"] = Follower.objects.filter(following=user,followed_by =self.request.user).exists()

        return context

class FollowView(LoginRequiredMixin,View):
    http_methods = ["POST"]
   
    def post(self,request,*args,**kwargs):
        data = request.POST.dict()
        if "action" not in data or "username" not in data:
            return HttpResponseBadRequest("Missing data")
        try:
            other_user = User.objects.get(username = data["username"])
                
        except User.DoesNotExist:
            return HttpResponseBadRequest("Missing user")

        if data["action"]  == "follow":
            follower, created = Follower.objects.get_or_create(
                followed_by = request.user,
                following = other_user
            )
        else:
            try:
                follower = Follower.objects.get(followed_by = request.user, following = other_user)

            except Follower.DoesNotExist:
                follower = None
            if follower:
                follower.delete()    
        return JsonResponse(
            {"success":True,
             "wording":"Unfollow"  if data["action"] == "follow" else "Follow",
             "total_following": Follower.objects.filter(following=other_user).count()
            }
        ) 

class UpdateProfileVeiw(LoginRequiredMixin,TemplateView):
 
    template_name = "profiles/update_profile.html"

    user_form = UserUpdateForm
    profile_form = ProfileUpdateForm

    def post(self, request,*args, **kwargs):
        
        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserUpdateForm(post_data, instance=request.user)
        profile_form = ProfileUpdateForm(post_data, file_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
     
            return HttpResponseRedirect(reverse_lazy('feed:home'))

        context = self.get_context_data(
                                        user_form=user_form,
                                        profile_form=profile_form
                                    )

                   

        return self.render_to_response(context)     

    def get(self, request, *args, **kwargs):
   
         return self.post(request, *args, **kwargs)


  




                          
                                 