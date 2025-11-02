from .models import UsersList, GroupUser, Post
from django.forms import ModelForm, Textarea, TextInput, EmailInput, SelectMultiple, Select


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

class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author_id', 'group_id', 'content']
        widgets = {
            'author_id': Select(attrs={
                'class': 'form-select',
                'placeholder': 'Выберите автора'
            }),
            'group_id': Select(attrs={
                'class': 'form-select',
                'placeholder': 'Выберите группу (необязательно)'
            }),
            'content': Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Введите текст поста...',
                'rows': 5
            }),
        }
        labels = {
            'author_id': 'Автор поста',
            'group_id': 'Группа',
            'content': 'Содержание поста',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group_id'].required = False
        self.fields['author_id'].queryset = UsersList.objects.all()
        self.fields['group_id'].queryset = GroupUser.objects.all()