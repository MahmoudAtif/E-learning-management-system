from .serializers import CheckoutSerializer , CourseSerializer , AuthorSerializer
from rest_framework import viewsets ,status
from rest_framework.views import APIView
from rest_framework.decorators import action
from app.models import Checkout ,Course , Author
from user.models import Student
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.http import Http404

class CheckoutView(viewsets.ModelViewSet):
    queryset=Checkout.objects.all()
    serializer_class=CheckoutSerializer
    permission_classes=[IsAuthenticated]
    lookup_url_kwarg = 'checkout_id'
    
    
    @action(detail=True , methods=['GET'])
    def student_checkouts(self , request , pk=None):
        try:
            student=Student.objects.get(id=pk)
            checkouts=Checkout.objects.filter(student=student.id)
            serializer=CheckoutSerializer(checkouts , many=True)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except:
            response={
                'message':'something wrong'
            }
            return Response(response , status=status.HTTP_404_NOT_FOUND)


class AuthorView(APIView):
    
    def get(self, request):
        queryset=Author.objects.all()
        serializer=AuthorSerializer(queryset, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer=AuthorSerializer(data=request.data)
        if serializer.is_valid:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_501_NOT_IMPLEMENTED)
            
class AuthorDetailView(APIView):
    def get_object(self, id):
        try:
            author=Author.objects.get(id=id)
            return author
        except Author.DoesNotExist:
            return None
    
    def get(self, request, id):
        author=self.get_object(id)
        serializer=AuthorSerializer(author)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        serializer=AuthorSerializer(data=serializer.data)
        if serializer.is_valid:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED)

    def delete(self, request, id):
        author=self.get_object(id)
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def search_api(request):
    try:
        queryset=Course.objects.filter(title__contains=request.data['query'])
        serializers=CourseSerializer(queryset, many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    except:
        response={
            'message':'not-found'
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)


class CourseView(APIView):
    def get(self,request):
        queryset=Course.objects.all()
        serializer=CourseSerializer(queryset,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer=CourseSerializer(data=request.data)
        if serializer.is_valid:
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_501_NOT_IMPLEMENTED)
    
class CourseViewDetails(APIView):
    permission_classes=[IsAuthenticated ]
    def get_object(self, id):
        try:
            course=Course.objects.get(id=id)
            return course
        except Course.DoesNotExist:
            return None
    
    def get(self, request, id):
        course=self.get_object(id)
        serializer=CourseSerializer(course)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,id):
        serializer=CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_304_NOT_MODIFIED)
    
    def delete(self, request, id):
        course=self.get_object(id)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

