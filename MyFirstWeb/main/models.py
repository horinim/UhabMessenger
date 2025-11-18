from django.db import models

class UsersList(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField('Имя пользователя',max_length=20)
    email = models.EmailField('Email пользователя')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Пользователь: {self.username}'

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Все пользователи'


class GroupUser(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Название группы',max_length=20)
    discription = models.TextField('Описание группы')
    users_list = models.ManyToManyField(
        UsersList,
        verbose_name="Участники группы",
        blank=True  # разрешить пустой список
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Группа: {self.name}'

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Все группы'

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    author_id = models.ForeignKey(UsersList, on_delete=models.CASCADE, verbose_name="ID автора:")
    group_id = models.ForeignKey(GroupUser, on_delete=models.SET_NULL, null=True, verbose_name="ID группы:")
    content = models.TextField(verbose_name="Информация в посте:")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Пост: {self.name}'

    @property
    def likes_count(self):
        return LikePost.objects.filter(post_id=self.id).count()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Все посты'

class CommentPost(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="ID поста:")
    author_id = models.ForeignKey(UsersList, on_delete=models.CASCADE, verbose_name="ID автора:")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Комментарий: {self.name}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Все комментарии'

class LikePost(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="ID поста:")
    author_id = models.ForeignKey(UsersList, on_delete=models.CASCADE, verbose_name="ID автора:")

    def __str__(self):
        return f'Лайк: {self.name}'

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Все лайки'