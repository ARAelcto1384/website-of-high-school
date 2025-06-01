from django.urls import path, include
from . import views
from django.contrib import auth

app_name = 'users'

urlpatterns = [
	path('login/', auth.views.LoginView.as_view(), name='login'),
    path('logout/', auth.views.LogoutView.as_view(), name='logout'),
    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth.views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth.views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth.views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth.views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
	path('my_account/', views.my_account, name='my_account'),
	path('my_account/edit_profile', views.my_accountep, name='my_accountep'),
    path('register/', views.register, name='register'),
]