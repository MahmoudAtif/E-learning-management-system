from rest_framework import serializers
from rest_framework.validators import ValidationError
from user.models import Student ,User
from django.contrib.auth import authenticate
from rest_framework import renderers , parsers
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

class SignInSerializer(serializers.Serializer):
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True)
    parser_classes=(
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )
    renderer_classes=(renderers.JSONRenderer,)
    
    def validate(self, attrs):
        username=attrs.get('username')
        password=attrs.get('password')
        if username and password:
            user=authenticate(username=username,password=password)
            if user is not None:
                if not user.is_active:
                    msg='user account is disabled'
                    raise serializers.ValidationError({
                        'status':'error',
                        'msg':msg
                    })
            else:
                msg='Unable to log in with provided crediential'
                raise serializers.ValidationError({
                    'status':'error',
                    'msg':msg
                })
        else:
            msg='Must include username and password'
            raise serializers.ValidationError({
                'status':'error',
                'msg':msg
            })
        attrs['user']=user
        return attrs




class SignUpSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=100 , write_only=True)
    is_student=serializers.BooleanField(required=True)
    is_instructor=serializers.BooleanField(required=True)
    
    class Meta:
        model=User
        fields=['id','username','email' , 'password' , 'is_student' , 'is_instructor']
        # extra_kwargs={
        #     'password':{
        #         'write_only':True
        #     }
        # }
    
    def create(self, validated_data):
        password=validated_data.pop('password', None)
        user=self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
            user.save()
            return user
    
    def validate(self, attrs):
        email_exists=User.objects.filter(email=attrs['email']).exists()
        if email_exists:
            raise ValidationError('Email has already been used')
        
        # if not attrs['is_student'] and not attrs['is_instructor']:
        #     raise ValidationError('You should select user type')       
        return super().validate(attrs) 


class ChangePasswordSerializer(serializers.Serializer):
   
    old_password=serializers.CharField(required=True)
    new_password=serializers.CharField(required=True)



class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields='__all__'
        

            