from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Импортируем модель, чтобы обратиться к ней
from .models import Post, Group
import datetime

# Create your views here.
SORTING = 10 

def year(request):
    """Добавляет переменную с текущим годом."""
    years = datetime.datetime.now()
    return {
        'year': years.year
    }
    
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
    }
    return render(request, 'posts/group_list.html', context) 

"""
def group_list(request):
    template = 'posts/group_list.html'
    context = {
        'title':"Здесь будет информация о группах проекта Yatube"
    }
    return render(request, template, context)
"""