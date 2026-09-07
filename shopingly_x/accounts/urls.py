from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('addresses/', views.address_list, name='address_list'),
    path('addresses/add/', views.address_add, name='address_add'),
    path('addresses/<int:pk>/delete/', views.address_delete, name='address_delete'),
]
