from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from .models import User
from .mixins import FieldsMixin,FormValidMixin,AuthorAccessMixin,SuperuserAccessMixin,AuthorsAccessMixin
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from blog.models import Article
from .forms import ProfileForm
# Create your views here.


class ArticleList(AuthorsAccessMixin,ListView):
    template_name='registration/home.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)

    
class ArticleCreate(AuthorsAccessMixin,FormValidMixin,FieldsMixin,CreateView):
    model = Article
    template_name = "registration/article-create-update.html"

class ArticleUpdate(AuthorAccessMixin,FormValidMixin,FieldsMixin,UpdateView):
    model = Article
    template_name = "registration/article-create-update.html"

class ArticleDelete(SuperuserAccessMixin,DeleteView):
    model = Article
    success_url = reverse_lazy('account:home')
    template_name="registration/article_confirm_delete.html"

class Profile(LoginRequiredMixin,UpdateView):
    model = User
    template_name = "registration/profile.html"
    success_url = reverse_lazy('account:profile')
    form_class=ProfileForm
    

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs=super(Profile,self).get_form_kwargs()
        kwargs.update({
            'user':self.request.user
        })
        return kwargs

class Login(LoginView):
    def get_success_url(self):
        user=self.request.user

        if user.is_superuser or user.is_author:
            return reverse_lazy('account:home')
        else:
            return reverse_lazy('account:profile')

