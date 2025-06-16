from django.urls import path
from . import views
from django.conf.urls import handler404


handler404 = 'notes.views.custom_404'

urlpatterns = [
    path('', views.home),
    path('login/', views.login_usr),
    path('register/', views.register),
    path('notes/', views.note_list),
    path('delete/<int:id>', views.delete, name='delete'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('signout/', views.signout),
]
