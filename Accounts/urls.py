from django.urls import path
# from .views import forgot_password, reset_password
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    
    path('password_reset/', passwordReset, name='password_reset'),
    path('password-reset-token/<uidb64>/<token>/', confirmToken, name='password_token_check'),
#    path('setPassword/<str:token>/', setPassword, name='password_reset_confirm'),

    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]