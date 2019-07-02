from django.urls import path, re_path
from django.conf.urls import url
from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', auth_view.LoginView.as_view(template_name='review/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='review/logout.html'), name='logout'),
    re_path(r'^category/(?P<cat_id>\d+)/(?P<rest_id>.+?)/$', views.restaurant_content, name='restaurant-content'),
    path('search_result/', views.search_result, name='search-result'),
    re_path(r'^update-review-likes/$',views.update_review_likes, name="update-review-likes"),
    re_path(r'^submit-a-review/$',views.submit_a_review, name="submit-a-review"),
    re_path(r'^comment-on-review/$',views.comment_on_review, name="comment-on-review"),
]