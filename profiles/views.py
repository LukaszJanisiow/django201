from django.contrib.auth.models import User
from django.views.generic import DetailView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseBadRequest
from feed.models import Post
from followers.models import Follower
from django.shortcuts import render, redirect
from django.core.paginator import Paginator



class ProfileDetailView(DetailView):
    http_method_names=["get"]
    template_name = "profiles/detail.html"
    model = User
    context_object_name = "user"
    slug_field = "username"
    slug_url_kwarg = "username" 

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self,**kwargs):
        user = self.get_object()
        context=super().get_context_data(**kwargs)
        context['total_posts'] = Post.objects.filter(author=user).count()
        context['total_followers']=Follower.objects.filter(following=user).count()
        if self.request.user.is_authenticated:
            context['you_follow'] = Follower.objects.filter(following=user, followed_by = self.request.user).exists()
        p = Paginator(Post.objects.filter(author=user).order_by('-id'), 5)
        page_number = self.request.GET.get('page')
        page_obj = p.get_page(page_number)
        context['posts'] = page_obj
        return context
    
class FollowView(LoginRequiredMixin,View):
    http_method_names=["post"]


    def post(self,request,*args,**kwargs):
        data=request.POST.dict()

        if "action" not in data or "username" not in data:
            return HttpResponseBadRequest("Missing data")
        
        try:
            other_user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return HttpResponseBadRequest("Missing user")
        
        if data['action'] == "Follow":
            follower, created = Follower.objects.get_or_create(
                followed_by =request.user,
                following = other_user
            )
        else:
            try:
                follower = Follower.objects.get(
                    followed_by =request.user,
                    following = other_user
                )
            except Follower.DoesNotExist:
                follower = None

            if follower:
                follower.delete()

        return JsonResponse({
            'success': True,
            'wording': "Unfollow" if data['action'] == "Follow" else "Follow"
        })
    
class AccountSettings(DetailView):
    model = User
    def get_context_data(self,**kwargs):
        user = self.request.user
        context={}
        context['total_posts'] = Post.objects.filter(author=user).count()
        context['total_followers']=Follower.objects.filter(following=user).count()
        return context
    
    def get(self, request):
        context = self.get_context_data()
        return render(request, "profiles/settings.html", context)
    
    def post(self,request):
        user=request.user
        user.username = request.POST.get('user_username')
        user.profile.text = request.POST.get('user_text')
        user.save()
        user.profile.save()
        return redirect('/profile/settings/')
    