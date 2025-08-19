from rest_framework import serializers
from app.models import Checkout, CheckoutItem, Section, Video, Course, Author
from user.models import Student
from django.db.models import Sum


class CheckoutItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckoutItem
        fields = "__all__"


class CheckoutSerializer(serializers.ModelSerializer):
    items = CheckoutItemSerializer(many=True)

    class Meta:
        model = Checkout
        fields = ["student", "price", "items"]


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"


class SectionSerializer(serializers.ModelSerializer):
    section_videos = VideoSerializer(read_only=True, many=True)

    class Meta:
        model = Section
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    course_sections = SectionSerializer(read_only=True, many=True)
    # is_enrolled=serializers.SerializerMethodField('get_enrollment')
    # duration=serializers.SerializerMethodField('get_duration')
    url = serializers.CharField(source="get_absolute_url", read_only=True)
    rating = serializers.IntegerField(source="get_rating", read_only=True)
    uploaded_videos = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False, use_url=False),
        write_only=True,
    )

    class Meta:
        model = Course
        fields = "__all__"
        # depth=1

    # def get_enrollment(self , course):
    #     user=self.context.get('request' , None).user
    #     student=Student.objects.get(student=user)
    #     return CheckoutItem.objects.filter(student=student, course=course).exists()

    # def get_duration(self , course):
    #     duration=course.course_videos.all().aggregate(sum=Sum('time_duration'))['sum']
    #     return duration


class AuthorSerializer(serializers.ModelSerializer):
    author_courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = "__all__"
