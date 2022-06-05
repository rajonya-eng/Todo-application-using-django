from django.contrib import admin
from django.urls import path
from .views import Task_list,Task_Detail,Task_Create,Task_Update,DeleteView,CustomLoginView,RegisterView,TaskReorder
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('login/',CustomLoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(next_page='login'), name='logout'),
    path('register/',RegisterView.as_view(), name='register'),
    path('', Task_list.as_view(), name="tasks"),
    path('task/<int:pk>/', Task_Detail.as_view(), name="task"),
    path('task-create/', Task_Create.as_view(), name='task-create'),
    path('task-update/<int:pk>/', Task_Update.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),
    path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),
]