from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('add/', views.add_student, name='add_student'),

    path('update/<int:id>/', views.update_student, name='update_student'),

    path('delete/<int:id>/', views.delete_student, name='delete_student'),

    path('upload/', views.upload_excel, name='upload_excel'),

    path('download/', views.download_students, name='download_students'),
]