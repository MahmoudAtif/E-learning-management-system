# from django.contrib.auth.models import User
from user.models import User
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from user.models import Student
from django.db.models import Avg, Sum
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, null=True,
                            blank=True, default='fa-solid fa-ghost')

    @property
    def get_total_courses(self):
        total = Course.objects.filter(category=self).count()
        if total:
            return total
        else:
            return 0

    def __str__(self):
        return self.name


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE,
                                  related_name='author_courses', limit_choices_to={'is_instructor': True})
    name = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to="author_images")
    description = models.TextField(null=True, blank=True)

    @property
    def get_total_courses(self):
        total = Course.objects.filter(author=self.id).count()
        return total

    @property
    def get_total_reviews(self):
        total = CommentCourse.objects.filter(course__author=self).count()
        return total

    @property
    def get_total_enrolments(self):
        total = CheckoutItem.objects.filter(course__author=self).count()
        return total

    @property
    def get_total_rating(self):
        total = CommentCourse.objects.filter(course__author=self).aggregate(
            average=Avg('rate'), sum=Sum('rate'))
        return total

    def __str__(self):
        return self.name


class Level(models.Model):
    name = models.CharField(max_length=50)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def get_total_courses(self):
        total = Course.objects.filter(level=self).count()
        return total

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=500)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    STATUS = (
        ('PUBLISH', 'PUBLISH'),
        ('DRAFT', 'DRAFT'),
    )

    CERTIFICATE = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )

    title = models.CharField(max_length=500)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='author_courses')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='course_category', )
    image = models.ImageField(upload_to="image")
    featured_video = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField()
    level = models.ForeignKey(
        Level, on_delete=models.CASCADE, null=True, blank=True)
    price = models.IntegerField(default=0)
    discount = models.IntegerField(null=True, blank=True, default=0)
    slug = models.SlugField(max_length=500, blank=True, unique=True)
    status = models.CharField(choices=STATUS, max_length=100, null=True)
    certificate = models.CharField(
        null=True, choices=CERTIFICATE, default='No', max_length=50)
    language = models.ForeignKey(Language, null=True, on_delete=models.CASCADE)
    favourite = models.ManyToManyField(User, blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    @property
    def get_total(self):
        total = self.price-(self.price * self.discount/100)
        return round(total, 2)

    @property
    def get_price_status(self):
        if self.price == 0:
            status = 'free'
        else:
            status = 'paid'
        return status

    @property
    def get_course_duration(self):
        videos = Video.objects.filter(course=self.id)
        duration = sum([video.time_duration for video in videos])

        if duration:
            total = duration
        else:
            total = 0

        return total

    @property
    def get_enrollment(self):
        total = CheckoutItem.objects.filter(course=self).count()
        return total

    @property
    def get_total_sections(self):
        total = Section.objects.filter(course=self.id).count()
        return total

    @property
    def get_total_videos(self):
        total = Video.objects.filter(course=self.id).count()
        return total

    # @property
    # def get_rating(self):
    #     rating=CommentCourse.objects.filter(course=self).aggregate(sum=Sum('rate') , average=Avg('rate'))
    #     return rating

    @property
    def get_rating(self):
        rating = CommentCourse.objects.filter(
            course=self).aggregate(average=Avg('rate'))['average']
        return rating

    @property
    def get_rating_sum(self):
        total = CommentCourse.objects.filter(course=self).count()
        return total

    @property
    def get_absolute_url(self):
        return reverse('course_details', kwargs={'slug': self.slug})

    # @property
    # def get_rating_average(self):
    #     course=CommentCourse.objects.filter(course=self).aggregate(average=Avg('rate'))
    #     average=course['average']
    #     return average

    def sections(self):
        return self.course_sections.all()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Skill(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='course_skills')
    point = models.CharField(max_length=100)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.course)


class Requirment(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='course_requirments')
    point = models.CharField(max_length=100)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.course)


class Section(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='course_sections')
    name = models.CharField(max_length=50)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.name} - {self.course}'


class Video(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='course_videos')
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name='section_videos')
    name = models.CharField(max_length=50)
    image = models.ImageField(
        upload_to='video_course_image', null=True, blank=True)
    serial_number = models.IntegerField(null=True, blank=True)
    youtube_id = models.CharField(max_length=200, null=True, blank=True)
    time_duration = models.IntegerField(null=True, blank=True)
    preview = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    @property
    def get_reviews_count(self):
        total = CommentVideo.objects.filter(video=self).count()
        return total

    def __str__(self):
        return f'{str(self.name)} - {str(self.course)} '


class ShopCart(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='student_carts')
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='student_courses')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f'{str(self.student)} - {str(self.course)}'


class Checkout(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='student_checkout')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.student)


class CheckoutItem(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='checkoutItems')
    checkout = models.ForeignKey(
        Checkout, on_delete=models.CASCADE, related_name='items')
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='enrolled_courses')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{str(self.checkout)} - {str(self.course)}'


class CommentCourse(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='student_comments')
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='course_comments')
    title = models.CharField(max_length=50)
    comment = models.TextField(max_length=100)
    rate = models.FloatField(default=0)
    like = models.ManyToManyField(Student, blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f'{str(self.student)} - {str(self.course)}'


class CommentVideo(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='student_video_comments')
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='course_video')
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name='video_comments')
    title = models.CharField(max_length=50)
    comment = models.TextField(max_length=100)
    like = models.ManyToManyField(Student, blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f'{str(self.student)} - {str(self.course)}'


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    content = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
