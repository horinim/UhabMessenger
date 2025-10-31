from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import UsersList, GroupUser
from .forms import UsersListForm, GroupUserForm

def index(request):
    data = {
        'title': 'Главная страница',
        'values': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
    }
    return render(request, 'main/index.html', data)

def about(request):
    return render(request, 'main/about.html')

def users_show(request):
    users = UsersList.objects.all()

    print("Количество пользователей:", users.count())
    for user in users:
        print(f"Пользователь: {user.username}, Email: {user.email}")

    context = {
        'users_list': users
    }
    return render(request, 'main/users_show.html', context)

def groups_show(request):
    groups_list = GroupUser.objects.all().order_by('-created_at')
    return render(request, 'main/groups_show.html', {'groups_list': groups_list})

def create_user(request):
    error = ''
    if request.method == 'POST':
        form = UsersListForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            error = 'Форма не верна'

    form = UsersListForm()
    data = {
        'form': form,
        'error': error,
    }
    return render(request, 'main/create_user.html', data)

def create_group(request):
    error = ''
    if request.method == 'POST':
        form = GroupUserForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            error = 'Форма не верна'

    form = GroupUserForm()
    data = {
        'form': form,
        'error': error,
    }
    return render(request, 'main/create_group.html', data)