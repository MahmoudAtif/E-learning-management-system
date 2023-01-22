from django.contrib import messages
from django.contrib.auth import login, logout , authenticate
# from django.contrib.auth.models import User
from .models import User
from django.shortcuts import redirect, render , HttpResponse

# from .backend import EmailBackEnd
from .forms import CreateUserForm,UserChangeForm
from django.http import HttpResponse
from.decorators import authenticated_user
from .send_mail import send_registration_message
# Create your views here.

@authenticated_user
def login_page(request):
    return render(request, 'login.html')


def login_func(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username , password=password)
        if user is not None:
            login(request , user)
            return redirect('/')
        else:
            messages.warning(request , 'username or password is incorrect')
            return redirect(request.META['HTTP_REFERER'])

    


@authenticated_user
def register(request):
    if request.method=='POST':
        user_type=request.POST.get('user-type')
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            form.username=request.POST.get('username')
            form.email=request.POST.get('email')
            form.password1=request.POST.get('password1')
            form.password2=request.POST.get('password2')   
            user.is_student=True            
            # if user_type == '1':
            #     user.is_student=True
            # else:
            #     user.is_instructor=True 
            send_registration_message(form.email)
            user.save()

            return redirect('login_page')
    else:
        form = CreateUserForm()
    context={
        'form':form
    }       
    return render(request , 'register.html',context)


def logout_page(request):
    logout(request)
    return redirect('home')



def profile(request):
    if request.method=='POST':
        form=UserChangeForm(request.POST)
        if form.is_valid:
            user=User.objects.get(id=request.user.id)
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            email=request.POST.get('email')
            username=request.POST.get('username')
            
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()
            messages.success(request , 'Profile updated successfully')
            return redirect('profile')

    return render(request , 'profile.html')



def for_test(request):
    return render(request, 'login.html')

