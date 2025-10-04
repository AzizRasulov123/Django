from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



class Category(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название')


    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'



class FAQ(models.Model):
    question = models.CharField(max_length=64, verbose_name='Вопрос')
    answer = models.TextField(max_length=64, verbose_name='Ответ')


    def __str__(self):
        return f'{self.question}, {self.answer}'


    class Meta:
        verbose_name = 'Вопрос и Ответ'
        verbose_name_plural = 'Вопросы и Ответы'


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    short_description = models.TextField(verbose_name='Краткое описание', blank=True, null=True)
    full_description = models.TextField(verbose_name='Полное описание')
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    is_visible = models.BooleanField(default=True, verbose_name='Статья активна?')
    preview = models.ImageField(upload_to='previews/articles/',
                                verbose_name='Заставка', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('details-page', kwargs={'details_id': self.pk})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    text = models.TextField(verbose_name='Коментарий')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.text[:30]}...'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Коментарии'


def make_article_image_path(instance, filename):
    return f'articles/{instance.article.pk}/{filename}'



class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    image = models.ImageField(upload_to=make_article_image_path, verbose_name='Фотография')


class Like(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='likes')
    user = models.ManyToManyField(User, related_name='likes')

class Dislike(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='dislikes')
    user = models.ManyToManyField(User, related_name='dislikes')


class ArticleViewsCount(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

