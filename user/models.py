# from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser , UserManager
from django.utils.translation import gettext_lazy as _



# limit_choices_to={'is_superuser': False}



class User(AbstractUser): 
    is_student = models.BooleanField(_('Student'),default=False)
    is_instructor = models.BooleanField(_('Instructor'),default=False)
    
    def __str__(self):
        return self.username

class Student(models.Model):
    student=models.ForeignKey(User, on_delete=models.CASCADE )
    name=models.CharField(null=True,blank=True,max_length=50)
    image=models.ImageField(upload_to='student/images', null=True , blank=True)
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.student)
    