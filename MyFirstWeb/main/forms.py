from .models import UsersList, GroupUser
from django.forms import ModelForm, Textarea, TextInput, EmailInput, SelectMultiple


class UsersListForm(ModelForm):
    class Meta:
        model = UsersList
        fields = ('username', 'email')

        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя',
            }),
            'email': EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@mail.com',
            })

        }

class GroupUserForm(ModelForm):
    class Meta:
        model = GroupUser
        fields = ('name', 'discription', 'users_list')

        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название группы',
            }),
            'discription': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание группы',
                'rows': 4,
            }),
            'users_list': SelectMultiple(attrs={
                'class': 'form-select users-multiselect',
                'size': 6,
            }),
        }

