from django.test import TestCase
from user.models import User, Student


class TestModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test", password="test", email="test@gmail.com"
        )
        self.student = Student.objects.create(
            student=self.user, name=self.user.username
        )

    def test_user_model(self):
        self.assertEqual(self.user.username, "test")
        self.assertEqual(self.user.email, "test@gmail.com")
        print("test_user_model ---> DONE")

    def test_student_model(self):
        self.assertEqual(self.student.name, "test")
        self.assertEqual(self.student.student.username, "test")
        self.assertEqual(self.student.student.email, "test@gmail.com")
        print("test_student_model ---> DONE")
