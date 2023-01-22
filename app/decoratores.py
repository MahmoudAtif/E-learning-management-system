from app.models import CheckoutItem, Video, Course
from user.models import Student
from django.shortcuts import redirect


def is_enrolled(view_func):
    def wrapper_func(request, *args, **kwargs):
        video_id = request.GET['video']
        video = Video.objects.get(id=video_id)
        student = Student.objects.get(student=request.user)
        if CheckoutItem.objects.filter(student=student, course=video.course.id).exists():
            return view_func
        else:
            return redirect(request.META['HTTP_REFERER'])
    return wrapper_func


def is_student(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_student:
            return view_func
        else:
            return redirect('home')
    return wrapper_func
