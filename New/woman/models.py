from django.db import models
from django.urls import reverse

# Create your models here.


class Woman(models.Model):
#всі стрічки тут це посилання на якийсь екземпляр класу, що працює завдяки
#механізму міграцій, щось типу python manage.py makemigrations...
    title = models.CharField(max_length=200, verbose_name='Заголовок')
#title - це посилання на екземпляр CharField()
    slug = models.SlugField(max_length=255, unique=True, db_index=True,
                            verbose_name='URL')
#slug створює текст в пошуковуму рядку url
    content = models.TextField(blank=True, verbose_name='Вміст')
#content - це посилання на екземпляр TextField()
    photo = models.ImageField(upload_to='photos/%Y/%m/%d',
                              verbose_name='Фото')
#verbose_name - зміна назви поля на сайті
    time_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Час створення')
    time_update = models.DateTimeField(auto_now=True,
                                       verbose_name='Час зміни')
    is_published = models.BooleanField(default=True,
                                       verbose_name='Стан розміщення')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT,
                            null=True, verbose_name='Розділ')
#cat - це посилання на екземпляр ForeignKey()


    def __str__(self):
        return self.title

    def get_absolute_url(self): #Також створює автоматичну кнопку в панелі admin
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Відомі жінки'
        verbose_name_plural = 'Відомі жінки'
        ordering = ['time_create', 'title']

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True,
                            verbose_name='Розділ')
    slug = models.SlugField(max_length=255, unique=True, db_index=True,
                            verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['id']

