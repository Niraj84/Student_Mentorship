from rest_framework import serializers
import re
from query.models import CustomUser,Mentor, Query

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['email'] = user.email
        return token




class RegisterSerializer(serializers.ModelSerializer):
    password2= serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model= CustomUser
        fields= ['email','first_name','last_name','password','password2']
        extra_kwargs= {
            'password':{'write_only': True}
        }   

    def save(self):
        user= CustomUser(
            email=self.validated_data['email'],
            )
        password= self.validated_data['password']
        password2= self.validated_data['password2']

        
        if not re.search('^(?=(.*\d){2,})(?=.*[!@#$%]{2,})[0-9a-zA-Z!@#$%]{8,}', password): 
            raise serializers.ValidationError({'password':'Password should contain minimum 8 letters, 2 numbers and 2 special chars'})

        if password!=password2:
            raise serializers.ValidationError({'password':'password must match'})
        
        user.set_password(password)
        user.save()
        
        return user

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= CustomUser
        fields= ['email','password']

class MentorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Mentor
        fields='__all__'

class QuerySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    mentor=serializers.StringRelatedField()
    
    class Meta:
        model=Query
        fields=['id','user','mentor','question_title','question','answer','upload_file','upload_date']

class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model=Query
        fields=['answer']