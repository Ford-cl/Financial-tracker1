from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
     path('update_profile_picture/', views.update_profile_picture, name='update_profile_picture'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('addbudget/', views.index, name='index'),
]
