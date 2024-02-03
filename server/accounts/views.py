from django.shortcuts import render
from rest_framework.response import Response
from .models import *
from .serializers import *
from random import randint
from rest_framework.views import APIView
from rest_framework import status
#-----------------------------------------------------------
messages_for_front = {
    'csrf_set' : 'اعتبارسنجی شد.',
    'email_duplicated' : 'ایمیل تکراری است.',
    'user_create' : 'کاربر ساخته شد و کد اعتبارسنجی ارسال شد.',
    'user_not_found' : 'کاربر پیدا نشد.',
    'image_updated' : 'عکس پروفایل اپدیت شد.',
    'code_sent' : 'کد ارسال شد.',
    'password_changed' : 'پسورد با موفقیت تغییر کرد.',
    'wrong_coode' : 'کد اعتبارسنجی نامعتبر است.',
}
#-----------------------------------------------------------
"""
    api's in api_views.py :

    1- UserCreateView --> Create User with Post Api

    3- UserDeleteView  --> delete a user with pk only for admins
    4- UserUpdateView --> update user information
    5- UserDetailPKView --> get a informations of a user with pk for admins
    6- UserDetailView --> get a informations of a user for self
    7- ProfileImageUpdateView  --> Update user image profile.

    8- PasswordChangeRequest  --> Password change request
    9- ChangePassword  --> It change user password if can_change_password is active.
    10- code_validation --> It checks whether the code is the same as the code in the database

    

    

    in urls for login:
    20- TokenObtainPairView
    21- TokenRefreshView
    
"""
#-----------------------------------------------------------
class UserCreateView(APIView):
    def post(self, request):
        """
        Create User with Post Api
        urls : domain.com/..../users/create/

        Sample json :
        {
        "email" : "TahaM8000@gmail.com",
        "full_name" : "Taha Mousavi",
        "password" : "1234jj5678"
        }

        """

        info = UserSerializer(data=request.data)
        code = randint(1000, 9999)

        if info.is_valid():

            # Check if the email is duplicated
            email = info.validated_data['email'].lower()
            if User.objects.filter(email=email).exists():
                return Response({'message': messages_for_front['email_duplicated']}, status=status.HTTP_400_BAD_REQUEST)

            User(email=email,
                 is_active=False,
                 full_name=info.validated_data['full_name'],
                 code=code).save()

            user = User.objects.get(email=email)
            user.set_password(info.validated_data['password'])
            user.save()

            # send Code to User
            # send_code_mail(email, code)

            return Response({'message': messages_for_front['user_create']}, status=status.HTTP_201_CREATED)
        else:
            return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
#-----------------------------------------------------------