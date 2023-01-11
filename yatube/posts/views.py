from django.shortcuts import render, get_object_or_404, redirect 
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Импортируем модель, чтобы обратиться к ней
from .models import Post, Group, User
from .forms import PostForm 
import datetime

# Create your views here.
SORTING = 10 

def year(request):
    """Добавляет переменную с текущим годом."""
    years = datetime.datetime.now()
    return years.year
years = year(year)

def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    # Если порядок сортировки определен в классе Meta модели,
    # запрос будет выглядеть так:
    # post_list = Post.objects.all()
    # Показывать по 10 записей на странице.
    paginator = Paginator(post_list, 10) 

    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')

    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    # Отдаем в словаре контекста
    context = {
        'page_obj': page_obj,
        'years': years
        
    }
    return render(request, 'posts/index.html', context) 

# View-функция для страницы сообщества:


@login_required #декоратор для проверки залогиененых пользователей
def group_posts(request, slug):
    # Функция get_object_or_404 получает по заданным критериям объект 
    # из базы данных или возвращает сообщение об ошибке, если объект не найден.
    # В нашем случае в переменную group будут переданы объекты модели Group,
    # поле slug у которых соответствует значению slug в запросе
    group = get_object_or_404(Group, slug=slug)

    # Метод .filter позволяет ограничить поиск по критериям.
    # Это аналог добавления
    # условия WHERE group_id = {group_id}
    posts = Post.objects.filter(group=group).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        #'posts': posts,
        'page_obj': page_obj,
        'years': years
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    # Здесь код запроса к модели и создание словаря контекста
    #author = get_object_or_404(Post, author=username)
    author = get_object_or_404(User, username=username) 
    posts = Post.objects.filter(author=author.id).order_by('-pub_date')
    #  page_obj = get_paginator(request, posts) 
    #posts = Post.objects.filter(author=username).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'posts': posts,
        'page_obj': page_obj,
        'years': years
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id) 
    # Здесь код запроса к модели и создание словаря контекста
    context = {
        'post': post,
        'years': years
    }
    return render(request, 'posts/post_detail.html', context)


@login_required 
def post_create(request): 
    form = PostForm(request.POST, files=request.FILES or None) 
    if request.method == 'POST': 

        if form.is_valid(): 
            post = form.save(commit=False) 
            post.author = request.user 
            post.save() 
            return redirect('posts:profile', request.user.username) 
    # form = PostForm() 
    template = 'posts/create_post.html' 
    context = { 
        'form': form,
        'years': years
    } 
    return render(request, template, context) 


@login_required 
def post_edit(request, post_id): 
    post = get_object_or_404(Post, id=post_id) 
    form = PostForm(request.POST or None, instance=post)

    if request.user != post.author: 
        return redirect('posts:post_detail', post_id) 

    if form.is_valid(): 
        form.save() 
        return redirect('posts:post_detail', post_id) 

    context = { 
        'form': form, 
        'is_edit': True, 
        'post': post,
        'years': years
    } 

    return render(request, 'posts/create_post.html', context)
"""
def group_list(request):
    template = 'posts/group_list.html'
    context = {
        'title':"Здесь будет информация о группах проекта Yatube"
    }
    return render(request, template, context)
"""