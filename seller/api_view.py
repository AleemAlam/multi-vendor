from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CreateUserSerializer
from rest_framework.exceptions import ValidationError
from .models import Item, Category
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

if Group.objects.count() == 0:
    it = ContentType.objects.get_for_model(Item)
    ct = ContentType.objects.get_for_model(Category)
    us = ContentType.objects.get_for_model(User)
    item_permission_1 = Permission.objects.get(name='Can view item',
                                    content_type=it)
    item_permission_2 = Permission.objects.get(name='Can add item',
                                    content_type=it)
    item_permission_3 = Permission.objects.get(name='Can change item',
                                    content_type=it)
    category_permission_1 = Permission.objects.get(name='Can view category',
                                    content_type=ct)
    category_permission_2 = Permission.objects.get(name='Can add category',
                                    content_type=ct)
    category_permission_3 = Permission.objects.get(name='Can change category',
                                    content_type=ct)
    user_permission_1 = Permission.objects.get(name='Can view user',
                                    content_type=us)
    user_permission_2 = Permission.objects.get(name='Can change user',
                                    content_type=us)
    seller = Group.objects.create(name='Seller')                                    
    seller.permissions.add(item_permission_1)
    seller.permissions.add(item_permission_2)
    seller.permissions.add(item_permission_3)
    seller.permissions.add(category_permission_1)
    seller.permissions.add(category_permission_2)
    seller.permissions.add(category_permission_3)
    seller.permissions.add(user_permission_1)
    seller.permissions.add(user_permission_2)


class SellerCreateView(APIView):
    def post(self, request):
        serializer = CreateUserSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            new_user = serializer.save()
            new_user.is_staff = True
            new_user.is_active = False
            new_user.save()
            data['response'] = "User Created Successfully"
            data['username'] = new_user.username
            data['email'] = new_user.email
        else:
            data = serializer.errors
        return Response(data)
