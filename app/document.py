from django_elasticsearch_dsl import Document
from app.models import Course
from django_elasticsearch_dsl.registries import registry


@registry.register_document
class CourseDocument(Document):

    class Index:
        name = 'courses'

    class Django:
        model = Course
        fields = ['title']
