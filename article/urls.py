from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'article'

urlpatterns = [
    path('category-list/', views.category_list, name='category_list'),

    path('category-detail/<int:id>/', views.category_detail, name='category_detail'),
    path('category-new/<int:father>/', views.new_category, name='new_category'),
    path('category-new/', views.new_category, name='new_category'),
    path('category-delete/<int:id>/', views.delete_category, name='delete_category'),
    path('category-update/<int:id>/', views.update_category, name='update_category'),

    path('article-detail/<int:id>/', views.article_detail, name='article_detail'),
    path('article-new/<int:father>/', views.new_article, name='new_article'),
    path('article-new/', views.new_article, name='new_article'),
    path('article-delete/<int:id>/', views.delete_article, name='delete_article'),
    path('article-update/<int:id>/', views.update_article, name='update_article'),
]

