from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views as api_views

router = DefaultRouter()
router.register("checkouts", api_views.CheckoutView, basename="checkouts_api")
# router.register('courses' , api_views.CourseView , basename='courses_api')
# router.register('authors' , api_views.AuthorView , basename='authors_api')


urlpatterns = [
    path("api/", include(router.urls)),
    path("search_api/", api_views.search_api, name="search_api"),
    path("apicourse/", api_views.CourseView.as_view(), name="api_course"),
    path(
        "apicourse/<int:id>/",
        api_views.CourseViewDetails.as_view(),
        name="api_course_details",
    ),
    path("apiauthor/", api_views.AuthorView.as_view(), name="api_author"),
    path(
        "apiauthor/<int:id>/",
        api_views.AuthorDetailView.as_view(),
        name="api_author_details",
    ),
]
