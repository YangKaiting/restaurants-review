from django.urls import path
from django.conf.urls import url

from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', auth_view.LoginView.as_view(template_name='review/login.html'), name='login'),
    url(r'^category/(?P<cat_id>\d+)//$', views.restaurant_list, name='restaurant-list'),
    url(r'^category/(?P<rest_id>.+?)/$', views.restaurant_content, name='restaurant-content'),
]