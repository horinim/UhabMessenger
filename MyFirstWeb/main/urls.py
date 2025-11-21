from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views

router = DefaultRouter()
router.register(r'api/users', views.UsersListViewSet)
router.register(r'api/groups', views.GroupListViewSet)
router.register(r'api/posts', views.PostViewSet)
router.register(r'api/comments', views.CommentViewSet)
router.register(r'api/likes', views.LikeViewSet, basename='likes')

urlpatterns = [
    path('', include(router.urls)),
    # path('', views.index, name='index'),
    # path('about', views.about, name='about'),
    # path('users/', views.users_show, name='users_show'),
    # path('users/create', views.create_user, name='create_user'),
    # path('groups/create', views.create_group, name='create_group'),
    # path('groups/', views.groups_show, name='groups_show'),
    # path('posts/', views.posts_show, name='posts_show'),
    # path('posts/create', views.create_post, name='create_post'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),







]