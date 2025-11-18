from pickle import FALSE

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import UsersList, GroupUser, Post, CommentPost, LikePost
from .forms import UsersListForm, GroupUserForm, PostCreateForm
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes, OpenApiExample
from .serializers import UsersListSerializer, GroupUserSerializer, PostSerializer, CommentPostSerializer, LikePostSerializer, LikePostRequestSerializer
from django.shortcuts import get_object_or_404

# def index(request):
#     data = {
#         'title': 'Главная страница',
#         'values': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
#     }
#     return render(request, 'main/index.html', data)
#
# def about(request):
#     return render(request, 'main/about.html')
#
# def users_show(request):
#     users = UsersList.objects.all()
#
#     print("Количество пользователей:", users.count())
#     for user in users:
#         print(f"Пользователь: {user.username}, Email: {user.email}")
#
#     context = {
#         'users_list': users
#     }
#     return render(request, 'main/users_show.html', context)
#
# def groups_show(request):
#     groups_list = GroupUser.objects.all().order_by('-created_at')
#     return render(request, 'main/groups_show.html', {'groups_list': groups_list})
#
# def create_user(request):
#     error = ''
#     if request.method == 'POST':
#         form = UsersListForm(request.POST)
#         if form.is_valid():
#             form.save()
#         else:
#             error = 'Форма не верна'
#
#     form = UsersListForm()
#     data = {
#         'form': form,
#         'error': error,
#     }
#     return render(request, 'main/create_user.html', data)
#
# def create_group(request):
#     error = ''
#     if request.method == 'POST':
#         form = GroupUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#         else:
#             error = 'Форма не верна'
#
#     form = GroupUserForm()
#     data = {
#         'form': form,
#         'error': error,
#     }
#     return render(request, 'main/create_group.html', data)
#
# def posts_show(request):
#     posts = Post.objects.all().select_related('author_id', 'group_id')
#     return render(request, 'main/posts_show.html', {'posts_list': posts})
#
#
# def create_post(request):
#     if request.method == 'POST':
#         form = PostCreateForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.save()
#     else:
#         form = PostCreateForm()
#
#     return render(request, 'main/create_post.html', {'form': form})



#Пользователи
@extend_schema_view(
    list=extend_schema(
        summary="Получить список всех пользователей",
        description="Возвращает полный список пользователей из базы данных"
    ),
    retrieve=extend_schema(
        summary="Получить пользователя по ID",
        description="Возвращает конкретного пользователя по его идентификатору"
    ),
    create=extend_schema(
        summary="Создать пользователя",
        description="Создает пользователя, который будет добавлен в БД",
        request=UsersListSerializer,
        responses={201: UsersListSerializer}
    ),
    update=extend_schema(
        summary="Полное обновление пользователя (PUT)",
        description="Требует отправки всех полей. Не указанные поля будут сброшены!"
    ),
    destroy=extend_schema(
        summary="Удаление пользователя",
        description="Пользователь будет удален из БД!!!",
        responses={
            204: None,
        }
    ),
)
class UsersListViewSet(viewsets.ModelViewSet):
    queryset = UsersList.objects.all()
    serializer_class = UsersListSerializer
    http_method_names = ['get', 'post', 'put', 'delete']



#Группы
@extend_schema_view(
    list=extend_schema(
        summary="Получить список всех групп",
        description="Возвращает полный список групп из базы данных"
    ),
    retrieve=extend_schema(
        summary="Получить группу по ID",
        description="Возвращает конкретную группу по ее идентификатору"
    ),
    create=extend_schema(
        summary="Создать группу",
        description="Создает группу, которая будет добавлен в БД",
        request=GroupUserSerializer,
        responses={201: GroupUserSerializer}
    ),
    update=extend_schema(
        summary="Полное обновление группы (PUT)",
        description="Требует отправки всех полей. Не указанные поля будут сброшены!"
    ),
    destroy=extend_schema(
        summary="Удаление группы",
        description="Группа будет удалена из БД!!!",
        responses={
            204: None,
        }
    ),
)
class GroupListViewSet(viewsets.ModelViewSet):
    queryset = GroupUser.objects.all()
    serializer_class = GroupUserSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    @extend_schema(
        summary="Добавить пользователя в группу",
        description="Добавляет пользователя в группу по его ID",
        parameters=[
            OpenApiParameter(
                name='user_id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID пользователя для добавления'
            )
        ],
        responses={
            200: GroupUserSerializer,
            400: {"type": "object", "properties": {"error": {"type": "string"}}},
            404: {"type": "object", "properties": {"error": {"type": "string"}}}
        }
    )
    @action(detail=True, methods=['post'], url_path='members/(?P<user_id>[^/.]+)')
    def add_member(self, request, pk=None, user_id=None):
        group = self.get_object()

        try:
            user = UsersList.objects.get(id=user_id)
        except UsersList.DoesNotExist:
            return Response(
                {"error": f"Пользователь с ID {user_id} не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        if group.users_list.filter(id=user_id).exists():
            return Response(
                {"error": f"Пользователь {user.username} уже в группе"},
                status=status.HTTP_400_BAD_REQUEST
            )

        group.users_list.add(user)

        serializer = self.get_serializer(group)
        return Response(serializer.data)

    @extend_schema(
        summary="Удалить пользователя из группы",
        description="Удаляет пользователя из группы",
        parameters=[
            OpenApiParameter(
                name='user_id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID пользователя'
            )
        ],
        responses={
            200: GroupUserSerializer,
            404: {"type": "object", "properties": {"error": {"type": "string"}}}
        }
    )
    @action(detail=True, methods=['delete'], url_path='members/(?P<user_id>[^/.]+)')
    def remove_member(self, request, pk=None, user_id=None):
        group = self.get_object()

        try:
            user = UsersList.objects.get(id=user_id)
        except UsersList.DoesNotExist:
            return Response(
                {"error": f"Пользователь с ID {user_id} не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not group.users_list.filter(id=user_id).exists():
            return Response(
                {"error": f"Пользователь {user.username} не состоит в группе"},
                status=status.HTTP_400_BAD_REQUEST
            )

        group.users_list.remove(user)

        serializer = self.get_serializer(group)
        return Response(serializer.data)



#Посты
@extend_schema_view(
    list=extend_schema(
        summary="Получить список всех постов",
        description="Возвращает полный список постов из базы данных"
    ),
    retrieve=extend_schema(
        summary="Получить пост по ID",
        description="Возвращает конкретный пост по его идентификатору"
    ),
    create=extend_schema(
        summary="Создать пост",
        description="Создает пост, который будет добавлен в БД",
        request=PostSerializer,
        responses={201: PostSerializer}
    ),
    update=extend_schema(
        summary="Полное обновление поста (PUT)",
        description="Требует отправки всех полей. Не указанные поля будут сброшены!"
    ),
    destroy=extend_schema(
        summary="Удаление поста",
        description="Пост будет удален из БД!!!",
        responses={
            204: None,
        }
    ),
)
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    http_method_names = ['get', 'post', 'put', 'delete']



#Комментарии
@extend_schema_view(
    list=extend_schema(
        summary="Получить список всех комментариев",
        description="Возвращает полный список комментариев из базы данных"
    ),
    create=extend_schema(
        summary="Создать комментарий",
        description="Создает комментарий, который будет добавлен в БД",
        request=CommentPostSerializer,
        responses={201: CommentPostSerializer}
    ),
    retrieve=extend_schema(
        summary="Получить комментарий по ID",
        description="Возвращает конкретный комментарий по его идентификатору"
    ),
    update=extend_schema(
        summary="Полное обновление комментария (PUT)",
        description="Требует отправки всех полей. Не указанные поля будут сброшены!"
    ),
    destroy=extend_schema(
        summary="Удаление комментария",
        description="Комментарий будет удален из БД!!!",
        responses={
            204: None,
        }
    ),
)
class CommentViewSet(viewsets.ModelViewSet):
    queryset = CommentPost.objects.all()
    serializer_class = CommentPostSerializer
    http_method_names = ['get', 'put','post', 'delete']

    @extend_schema(
        summary="Получить комментарии к посту",
        description="Возвращает все комментарии для конкретного поста",
        responses={200: CommentPostSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='posts/(?P<post_id>[^/.]+)')
    def get_post_comments(self, request, post_id=None):
        comments = CommentPost.objects.filter(post_id=post_id)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)



#Лайки
class LikeViewSet(viewsets.ViewSet):

    @extend_schema(
        summary="Получить лайки к посту",
        description="Возвращает все лайки для конкретного поста",
        parameters=[
            OpenApiParameter(
                name='post_id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID поста'
            )
        ],
        responses={200: LikePostSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='posts/(?P<post_id>[^/.]+)/likes/count')
    def get_post_likes(self, request, post_id=None):
        likes = LikePost.objects.filter(post_id=post_id)
        serializer = LikePostSerializer(likes, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Добавить лайк",
        description="Создает лайк, который будет добавлен в БД",
        request=LikePostRequestSerializer,
        responses={
            201: LikePostSerializer,
            400: {"type": "object", "properties": {"error": {"type": "string"}}},
            404: {"type": "object", "properties": {"error": {"type": "string"}}}
        }
    )
    @action(detail=False, methods=['post'], url_path='posts/(?P<post_id>[^/.]+)/like')
    def add_post_like(self, request, post_id=None):
        request_serializer = LikePostRequestSerializer(data=request.data)
        if not request_serializer.is_valid():
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"error": f"Пост с ID {post_id} не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        author_id = request.data.get('author_id')
        if not author_id:
            return Response(
                {"error": "author_id обязателен в теле запроса"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = UsersList.objects.get(id=author_id)
        except UsersList.DoesNotExist:
            return Response(
                {"error": f"Пользователь с ID {author_id} не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        if LikePost.objects.filter(post_id=post_id, author_id=author_id).exists():
            return Response(
                {"error": f"Пользователь {user.username} уже поставил лайк на этот пост"},
                status=status.HTTP_400_BAD_REQUEST
            )

        like = LikePost.objects.create(post_id=post, author_id=user)

        serializer = LikePostSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Удалить лайк по ID",
        description="Удаляет лайк по его идентификатору",
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID лайка'
            )
        ],
        responses={204: None}
    )
    def destroy(self, request, pk=None):
        try:
            like = LikePost.objects.get(id=pk)
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except LikePost.DoesNotExist:
            return Response(
                {"error": f"Лайк с ID {pk} не найден"},
                status=status.HTTP_404_NOT_FOUND
            )