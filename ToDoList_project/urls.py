"""
URL configuration for ToDoList_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', views.get_users, name='get_users'),
    path('users/create', views.create_user, name='create_user'),
    path('users/user-detail/<int:telegram_id>', views.user_detail, name='user_detail'),
    path('user-tasks/<int:telegram_id>', views.get_user_tasks, name='get_user_tasks'),
    path('user-tasks/create', views.create_user_task, name='create_user_task'),
    path('user-tasks/detail/<int:pk>', views.user_task_detail, name='user_task_detail'),
    path('categories/', views.get_categories, name='get_categories'),
    path('categories/create', views.create_category, name='create_category'),
]
