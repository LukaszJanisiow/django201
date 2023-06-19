from django.views.generic import TemplateView, DetailView, View
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from django.http import HttpResponse



from .models import Post
from followers.models import Follower

class HomePage(TemplateView):
    template_name = "feed/homepage.html"

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:
            user=self.request.user
            context['followed_World'] = user.profile.followed_World
            if user.profile.followed_World:
                following = list(Follower.objects.filter(followed_by=self.request.user).values_list('following', flat = True))
                following.append(self.request.user)
                context['posts'] = Post.objects.filter(author__in=following).order_by('-id')[0:60]
            else:
                 context['posts'] = Post.objects.all().order_by('-id')[0:30]
        else:
            context['posts'] = Post.objects.all().order_by('-id')[0:30]
        return context
    
    def post(self, request):
        # Handle the form submission logic here
        user=request.user
        if request.POST['answer'] == "followed":
            user.profile.followed_World = True
        elif request.POST['answer'] == "world":
            user.profile.followed_World = False
        user.save()
        user.profile.save()
        return redirect('/')

        
    

class PostDetailView(DetailView):
    http_method_names =["get"]
    template_name = "feed/detail.html"
    model = Post
    context_object_name = "post"

class CreateNewPost(LoginRequiredMixin, CreateView ):
    model = Post
    template_name = "feed/create.html"
    fields = [
        'text' ]
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self,form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super().form_valid(form)

    def post(self, request,*args,**kwargs):
        post = Post.objects.create(
            text=request.POST.get("text"),
            author=request.user,
        )
        return render(
            request,
            "includes/post.html",
            {
                "post" : post,
                "show_detail_link": True,

            },
            content_type="application/html"
        )
    
