from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *

# Create your views here.

class WomanHome(DataMixin, ListView):
    model = Woman
    template_name = 'woman/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Головна сторінка')
        return context | c_def

    def get_queryset(self):
        return Woman.objects.filter(is_published=True).select_related('cat')

# def index(request): #HttpRequest, request це не випадкова назва
#     posts = Woman.objects.all()
#     context = {'posts': posts,
#                'menu': menu,
#                'title': 'Головна сторінка',
#                'cat_selected': 0}
#     return render(request, 'woman/index.html', context)

def about(request):
    contact_list = Woman.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'woman/about.html',
                  {'page_obj': page_obj, 'menu': menu,
                   'title': 'Не про сайт'})

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'woman/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Додати статтю')
        return context | c_def

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#                 form.save()
#                 return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request,
#                   'woman/addpage.html',
#                   {'form': form,
#                    'menu': menu,
#                    'title': 'Добавлення статті'})

# def contact(request):
#     return HttpResponse('Зворотній зв\'язок')

class ContactFormViev(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'woman/contact.html'
    succes_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Зворотній зв\'язок')
        return context | c_def

    def form_valid(selfself, form):
        print(form.cleaned_data)
        return redirect('home')
# def login(request):
#     return HttpResponse('Авторизація')

def pageNotFound(request, exception): #exception це не випадкова назва
    return HttpResponseNotFound('<h1>Сторінку не знайдено</h1>')

class ShowPost(DataMixin, DetailView):
    model = Woman
    template_name = 'woman/post.html'
    slug_url_kwarg = 'post_slug'
    #pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return context | c_def



# def show_post(request, post_slug):
#     post = get_object_or_404(Woman, slug=post_slug)
#
#     context = {'post': post,
#                'menu': menu,
#                'title': post.title,
#                'cat_selected': post.cat_id
#
#     }

#     return render(request, 'woman/post.html', context=context)

class WomanCategory(DataMixin, ListView):
    model = Woman
    template_name = 'woman/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Woman.objects.filter(cat__slug=self.kwargs['cat_slug'],
                                    is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(
            title='Розділ - ' +
            str(c.name),
            cat_selected=c.pk)
        return context | c_def

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'woman/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Реєстрація')
        return context | c_def

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'woman/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизація')
        return context | c_def

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')


# def show_category(request, cat_slug):
#     posts = Woman.objects.filter(cat__slug=cat_slug)
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {'posts': posts,
#                'menu': menu,
#                'title': 'Відображення по розділам',
#                'category_selected': cat_slug}
#     return render(request, 'woman/index.html', context)

# def categories(request, cats): #cats\number
#     if request.POST:
#         print(request.POST)
#     return HttpResponse(f'<h1>Статті по категоріям</h1><p>{cats}</p>')
#
# def archive(request, year):
#     if int(year) > 2020:
#         #return redirect('/', permanent=True) #перехід на головну сторінку
#         return redirect('home', permanent=True)
#     return HttpResponse(f'<h1>Архів по рокам <\h1><p>{year}</p>')
