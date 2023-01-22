from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views as api_views

router = DefaultRouter()
router.register('students', api_views.StudentViewset)
# router.register('users',api_views.SignUpViewset)

urlpatterns = [
    path('api-auth', include('rest_framework.urls')),
    path('api-auth-token/', obtain_auth_token),
    path('api/', include(router.urls)),
    path('signupapi/', api_views.SignUpView.as_view(), name='signup_api'),
    path('signinapi/', api_views.SignInView.as_view(), name='signin_api'),
    path('change-password-api/', api_views.ChangePasswordView.as_view(),
         name='change_password_api'),
    path('reset-password/', include('django_rest_passwordreset.urls')),
    # path('reset-password-confirm-view/',api_views.ResetPasswordConfirmView.as_view(),name='reset_password_confirm_view'),

]
