from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from .views import *


urlpatterns = [
#path('', cache_page(60)(WomanHome.as_view()), name='home'), #http://127.0.0.1:8000/
#кешування (затримка оновлення) сторінки на 60 секунд
    path('', WomanHome.as_view(), name='home'), #http://127.0.0.1:8000/
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormViev.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', WomanCategory.as_view(), name='category'),

    # path('cats/<slug:cats>', categories), #http://127.0.0.1:8000/cats/
    # re_path(r'^archive/(?P<year>[0-9]{4})/', archive)
]

