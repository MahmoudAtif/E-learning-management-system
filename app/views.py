from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView , DetailView
from app.models import (Author, Category, Checkout, CheckoutItem,
                        CommentCourse, Course, Level, ShopCart, Video,CommentVideo , Question)
from user.models import Student

from .decoratores import *

from .functions import check_price


# Create your views here.

# class Home(ListView):
#     model=Course
#     context_object_name='courses'
#     queryset=Course.objects.filter(status="PUBLISH")
#     template_name='pages/home.html'
    
#     def post(self , request):
#         email=request.POST.get('email')
#         password=request.POST.get('password')
#         user=authenticate(request,username=email , password=password)
#         if user is not None:
#             login(request , user)
#             return redirect('home')
#         else:
#             messages.warning(request , 'username or password is incorrect')
    

# class Home(View):
#     def get(self , request):
#         courses=Course.objects.filter(status="PUBLISH")
#         context={
#             'courses':courses,
#         }
#         return render(request , 'pages/home.html',context)
    
#     def post(self , request):
#         email=request.POST.get('email')
#         password=request.POST.get('password')
#         user=authenticate(request,username=email , password=password)
#         if user is not None:
#             login(request , user)
#             return redirect('home')
#         else:
#             messages.warning(request , 'email or password is incorrect')

def home(request):
    courses=Course.objects.filter(status="PUBLISH")
    instructors=Author.objects.all()[:5]        
    context={
        'courses':courses,
        'instructors':instructors,
    }
    return render(request , 'pages/home.html',context)
    
def courses(request):
    levels=Level.objects.all()
    queryset=Course.objects.filter(status="PUBLISH")
    authors=Author.objects.filter()[:4]

    freeCourses_count=Course.objects.filter(price=0).count()
    paidCourses_count=Course.objects.filter(price__gte=1).count()
    
    ############## Pagination ###########
    page=request.GET.get('page',1)
    paginator=Paginator(queryset , 10)
    try:
        courses=paginator.page(page)
    except:
        courses=paginator.page(1)
    ############## EndPagination ###########
    

    context={   
        'courses':courses,
        'authors':authors,
        'levels':levels,
        'freeCourses_count':freeCourses_count,
        'paidCourses_count':paidCourses_count,

    }
    return render(request , 'pages/courses.html',context)

def contact(request):
    if request.method =='POST':
        Question.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            content=request.POST.get('content'),
        )
        return HttpResponse('Thanks for you question')
    return render(request , 'pages/contact_us.html')


def about(request):
    return render(request , 'pages/about.html')


def filter_data(request):
    category=request.GET.getlist('category[]')
    level= request.GET.getlist('level[]')
    price=request.GET.getlist('price[]')
    
    if price== ['priceall']:
        courses=Course.objects.filter(status="PUBLISH")
    elif price== ['pricefree']:
        courses=Course.objects.filter(price=0)
    elif price== ['pricepaid']:
        courses=Course.objects.filter(price__gte=1)
    elif category:
        courses=Course.objects.filter(category__id__in=category)
    elif level:
        courses=Course.objects.filter(level__id__in=level)
    t = render_to_string('pages/courses.html' , {'courses':courses})
    return JsonResponse({'data': t})



def search(request):  
    search=request.GET['search']
    courses=Course.objects.filter(title__contains=search)
    
    context={
        'courses':courses,
        }
    return render(request , 'pages/search.html',context)


def course_details(request, slug):
    
    try:
        course=Course.objects.get(slug=slug)
    except Course.DoesNotExist:
        return redirect('not_found')
    related_courses=Course.objects.filter(category=course.category).order_by('-id')
    latest_courses=Course.objects.filter(author=course.author).order_by('-id')[:3] 
    
    try: 
        student=request.user.student
        enroll_course=student.checkoutItems.get(course=course)  
    except CheckoutItem.DoesNotExist:
        enroll_course=None
    
    try:
        cart=ShopCart.objects.get(student=student, course=course)
    except ShopCart.DoesNotExist:
        cart=None

    context={
        'course':course,
        'related_courses':related_courses,
        'latest_courses':latest_courses,
        'enroll_course':enroll_course,
        'cart':cart,
    }
    return render(request , 'pages/course_details.html',context)

def add_review(request,slug):
    if request.method =='POST':
        course=Course.objects.get(slug=slug)
        rating=request.POST.get('rating')
        title=request.POST.get('title')
        comment=request.POST.get('comment')
        if request.user.is_authenticated:
            student=Student.objects.get(student=request.user)
            new_comment=CommentCourse()
            new_comment.student=student
            new_comment.course=course
            new_comment.title=title
            new_comment.comment=comment
            new_comment.rate=rating
            if not CommentCourse.objects.filter(student=student , course=course):
                new_comment.save()
                return HttpResponse('Success Review')
            else:
                return HttpResponse('you are already Reviewed')

        else:
            messages.warning(request , 'Login required')
    return redirect(request.META['HTTP_REFERER'])
    

def not_found(request):
    return render(request , 'pages/not_found.html')


@login_required(login_url='login_page')
def enrolled_free_course(request,slug):
    course=Course.objects.get(slug=slug)
    student=request.user.student
    if course.price==0:
        if not CheckoutItem.objects.filter(student=student , course=course):
            checkout=Checkout()
            checkout.student=student
            checkout.price=course.price
            checkout.save()

            CheckoutItem.objects.create(
                student=student,
                checkout=checkout,
                course=course,
                price=course.price
            )
            messages.success(request , 'Course Successfully Enrolled')
        
        else:
            print('exist')
    else:
        pass
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='login_page')
def add_to_cart(request , slug):
    course=Course.objects.get(slug=slug)
    student=request.user.student
    if not ShopCart.objects.filter(student=student,course=course):
        ShopCart.objects.create(
            student=student,
            course=course,
            price=check_price(course),
            )
    return redirect('shop_cart')
   

def remove_cart(request , slug):
    course=Course.objects.get(slug=slug)
    student=request.user.student
    cart=ShopCart.objects.get(student=student ,course=course)
    cart.delete()
    return redirect(request.META['HTTP_REFERER'])

def shop_cart(request):
    context={
    }
    return render(request , 'pages/shop_cart.html',context)

@login_required(login_url='login_page')
def checkout(request):
    if request.user.is_authenticated:
        student=request.user.student
        carts=ShopCart.objects.filter(student=student)
        total_price=0
        for item in carts:
            if item.course.discount:
                total_price+=item.course.get_total
            else:
                total_price+=item.course.price
        
        if request.method=='POST':
            checkout=Checkout()
            checkout.student=student
            checkout.price=total_price
            checkout.save()
            
            for item in carts:
                if item.course.discount:
                    price=item.course.get_total
                else:
                    price=item.course.price
                CheckoutItem.objects.create(
                    student=student ,
                    checkout=checkout,
                    course=item.course,
                    price=price
                )
                item.delete()
            return redirect('checkout_complete' , checkout.id)
    else:
        carts=None
    context={
        'carts':carts,
        'total_price':total_price
    }
    return render(request , 'pages/checkout.html',context)

class CheckoutComplete(DetailView):
    template_name='pages/completed.html'
    model=Checkout
    context_object_name='checkout'
    pk_url_kwarg = 'id'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['checkout_complete']= True
        return context


# class MyCourses(ListView):
#     model=CheckoutItem
#     template_name='pages/mycourses.html'
#     context_object_name='courses'

#     def get_queryset(self):
#         qs=super().get_queryset()
#         student=Student.objects.get(student=self.request.user)
#         return qs.filter(student=student)


def my_courses(request):
    try:
        student=request.user.student
        courses=student.checkoutItems.all()
    except:
        return redirect('not_found')
    context={
        'courses':courses
    }
    return render(request , 'pages/mycourses.html',context)

def favourite(request):
    courses=Course.objects.filter(favourite=request.user)
    context={
        'courses':courses
    }
    return render(request , 'pages/favourite.html',context)

def instructor_details(request,id):
    instructor=Author.objects.get(id=id)
    context={
        'instructor':instructor
    }
    return render(request , 'pages/instructor_details.html',context)

@login_required(login_url='login_page')
def add_to_favourite(request,slug):
    course=Course.objects.get(slug=slug)
    if request.user in course.favourite.all():
        course.favourite.remove(request.user)
    else:    
        course.favourite.add(request.user)

    return redirect(request.META['HTTP_REFERER'])


def watch_course(request , slug):
    course=Course.objects.get(slug=slug)
    
    try: 
        video_id=request.GET.get('video')
        video=Video.objects.get(id=video_id)
    except:
        video=None
    try:
        student=request.user.student
        enroll_course=student.checkoutItems.get(student=student , course=course)
    except CheckoutItem.DoesNotExist:
        enroll_course=None
    

    context={
        'watch_course':'watch_course',
        'course':course,
        'enroll_course':enroll_course,
        'video':video,
    }
    return render(request , 'pages/watch_course.html',context)


def video_review(request , id ,slug):
    # video_id=request.GET.get('video')
    video=Video.objects.get(id=id)
    if request.method =='POST':
        course=Course.objects.get(slug=slug)
        title=request.POST.get('title')
        comment=request.POST.get('comment')
        if request.user.is_authenticated:
            student=Student.objects.get(student=request.user)
            new_comment=CommentVideo()
            new_comment.student=student
            new_comment.course=course
            new_comment.video=video
            new_comment.title=title
            new_comment.comment=comment
            if not CommentVideo.objects.filter(student=student , course=course , video=video):
                new_comment.save()
                
        else:
            messages.warning(request , 'Login required')
   
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='login_page')
def buy_now(request,slug):
    course=Course.objects.get(slug=slug)
    student=request.user.student
    if not course in ShopCart.objects.filter(student=student):
        ShopCart.objects.create(
        student=student,
        course=course,
        price=check_price(course)
        )
    return redirect('checkout')







