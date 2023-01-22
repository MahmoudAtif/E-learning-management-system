# from django.contrib.auth.models import User
# from django.contrib.auth.backends import ModelBackend
# from django.db.models import Q

# class EmailBackEnd(ModelBackend):
#     def authenticate(self,  username=None, password=None, **kwargs):
#         # UserModel = get_user_model()
#         try:
#             # to login with username or email
#             user = User.objects.get( Q(username__iexact=username)| Q(email__iexact=username))
#         except User.DoesNotExist:
#             return None
#         else:
#             if user.check_password(password):
#                 return user
#         return None

#     def get_user(self , user_id):
#         try:
#             user = User.objects.get(pk=user_id)

#         except User.DoesNotExist:
#             return None
#         return user if self.user_can_authenticate(user) else None
