from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),    
    path('blog/',views.home, name='home'),
    path('blogs/',views.blog_list, name='blog_list'),
    path('blogs/<int:id>/', views.blog_detail, name='blog_detail'),
    path('blog/create/', views.blog_create, name='blog_create'),
    path('blog/<int:id>/update/', views.blog_update, name='update_blog'),
    path('blog/<int:id>/delete/', views.blog_delete, name='blog_delete'),
    path('posts/create/', views.post_create, name='post_create'),
    path('posts/<int:id>/update/', views.post_update, name='post_update'),
    path('posts/<int:id>/delete/', views.post_delete, name='post_delete'),
    path('logout/', views.logout_view, name='logout'),

]