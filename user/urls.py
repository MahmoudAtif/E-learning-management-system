from django.contrib.auth import views as auth_views
from django.urls import path ,include

from . import views

urlpatterns = [
    path('login/' , views.login_page , name='login_page'),
    path('login-func/' , views.login_func , name='login_func'),
    path('register/' , views.register , name='register'),
    path('logout/' , views.logout_page , name='logout'),
    # path('accounts/', include('allauth.urls')),
    
    path('password_reset_form/' ,auth_views.PasswordResetView.as_view(template_name='forgot_password/password_reset_form.html') ,name='password_reset_form'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='forgot_password/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='forgot_password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='forgot_password/password_reset_complete.html'), name='password_reset_complete'),
    
    
    path('profile/' , views.profile , name='profile'),
    path('for_test/' , views.for_test , name='for_test'),

]
