
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from survey_game import views as survey_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', survey_views.register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('survey_game.urls')),
]
