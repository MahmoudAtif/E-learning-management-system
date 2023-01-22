from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('' , views.Home.as_view() , name='home'),
    path('courses/', views.courses, name='courses'),
    path('courses/filter-data/', views.filter_data, name='filter-data'),
    path('search/', views.search, name='search'),
    path('course/<slug:slug>/', views.course_details, name='course_details'),

    path('not-found/', views.not_found, name='not_found'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('enrolled_free_course/<slug:slug>/',
         views.enrolled_free_course, name='enrolled_free_course'),

    path('my-courses/', views.my_courses, name='my_courses'),
    # path('my-courses/',views.MyCourses.as_view() , name='my_courses'),

    path('favourites/', views.favourite, name='favourite'),
    path('shop-cart/', views.shop_cart, name='shop_cart'),
    path('add-to-cart/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('buy-now/<slug:slug>/', views.buy_now, name='buy_now'),
    path('add-to-favourite/<slug:slug>/',
         views.add_to_favourite, name='add_to_favourite'),
    path('remove-cart/<slug:slug>/', views.remove_cart, name='remove_cart'),
    path('checkout/', views.checkout, name='checkout'),
    # path('checkout-completed/<int:id>/' , views.checkout_complete , name='checkout_complete'),
    path('checkout-completed/<int:id>/',
         views.CheckoutComplete.as_view(), name='checkout_complete'),
    path('instructor_details/<int:id>/',
         views.instructor_details, name='instructor_details'),
    path('course/watch-course/<slug:slug>/',
         views.watch_course, name='watch_course'),


]


htmx_urlpattenrs = [
    path('add-review/<slug:slug>/', views.add_review, name='add_review'),
    path('video-review/<int:id>/<slug:slug>/',
         views.video_review, name='video_review'),

]


urlpatterns += htmx_urlpattenrs
