from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
from decimal import Decimal
from django.db.models import Q
from seller.serializers import CreateUserSerializer
from django.utils import timezone
import datetime

# REST api
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models
from . import serializers

import random
from twilio.rest import Client



#---------------------CUSTOMER PROFILE--------------------------


def send_otp(phone):
    if phone:
        otp = get_otp(phone)
        if otp:                    
            account_sid = "ACff0c8f7318f65e462d2c97cf9cb6a55f"
            auth_token  = "4e4574e533fdd6490d24c789e3172de6"

            client = Client(account_sid, auth_token)

            message = client.messages.create(
                to=str(phone), 
                from_="+15417028030",
                body="Your otp is "+str(otp))
            return otp
    else:
        return False
            
        

def get_otp(phone):
    if phone:
        otp = random.randint(999,9999)
        return otp
    else:
        return False



class CustomerCreateView(APIView):
    def post(self, request):
        data = request.data
        try:
            new_user = User.objects.create_user(
                username = data['username'],
                password = data['password'],
                first_name = data['first_name'],
                last_name = data['last_name'],
                is_active=False,
            )
            try:
                new_user.email = data['email']
                new_user.save()
            except:
                new_user.delete()
                return Response({'error': 'Email is already exist'})
        except:
            return Response({'error': 'username is already exists'})
        phone = data['mobile']
        if phone:
            check_phone = models.CustomerPhone.objects.filter(mobile = phone, is_verified = True)
            if check_phone.exists():
                new_user.delete()
                raise ValidationError('Phone is already exists')
            else:
                otp = send_otp(phone)
                if otp:
                    models.PhoneOTP.objects.create(
                        mobile=phone,
                        otp = otp
                    )
                    models.CustomerPhone.objects.create(mobile = phone, user=new_user)
                    return Response({
                        'message': 'OTP Sent Successfully',
                    })
                else:
                    return Response({
                        'message': 'OTP Error'
                    })
        else:
            return Response({
                        'message': 'Phone Number must be in Post method'
                    })


class ValidateOTP(APIView):
    def post(self, request, *args, **kwargs):
        phone = request.data.get('mobile')
        otp = request.data.get('otp')
        if phone and otp:
            phone_otp = models.PhoneOTP.objects.get(mobile = phone)
            if phone_otp.otp == otp:
                phone = models.CustomerPhone.objects.get(mobile = phone)
                phone.is_varified = False
                phone.is_varified = True
                phone.save()
                user = User.objects.get(username = phone.user.username )
                user.is_active = True
                user.save()
                phone_otp.delete()
                return Response({
                    'message': 'User Registered'
                })
            else:
                return Response({
                    'message': 'Invalid OTP'
                }) 
        else:
            return Response({
                'message': 'OTP is required'
            })



class ResendOTP(APIView):
    def post(self, request):
        phone = request.data.get('mobile')
        try:
            phone_obj = models.PhoneOTP.objects.get(mobile=phone)
        except :
            raise ValidationError('Invalid Phone')
        otp = send_otp(phone)
        if otp:
            phone_obj.otp = otp
            phone_obj.save()
            return Response({
                'message': 'OTP Resent Successfully',
            })
        else:
            return Response({
                'message': 'OTP Error'
            })


class UpdateNumber(APIView):
    def put(self, request, pk=None):
        data = request.data
        try:    
            account = models.CustomerPhone.objects.get(pk=pk)
        except:
            raise ValidationError('User Not Found')
        phone = data['mobile']
        if phone:
            check_phone = models.CustomerPhone.objects.filter(mobile = phone, is_varified = True)
            if check_phone.exists():
                if account != check_phone[0]:
                    return Response({
                        'message': 'Phone number is already exist'
                    })
                else:
                    return Response({
                        'message': 'This phone is already registered by you'
                    })

            else:
                otp = send_otp(phone)
                if otp:
                    models.PhoneOTP.objects.create(
                            mobile=phone,
                            otp = otp
                        )
                    account.mobile = phone
                    account.is_verified = False
                    account.save()
                    return Response({
                        'message':'OTP Send'
                    })
                else:
                    return Response({
                        'message': 'OTP Error'
                    })


class ProfileView(APIView):

    def res_content(self, user):
        return {
            "firstName": user.first_name,
            "lastName": user.last_name,
            "phone": user.phone.mobile if user.phone.is_verified else "",
            "email": user.email,
            "id": user.id,
            "addresses": [
                {
                    "id": a.id,
                    "flatNo": a.flat_no,
                    "street": a.street,
                    "area": a.area,
                    "locality": a.locality,
                } for a in user.address_set.all()
            ]
        }

    def get(self, request, format=None, **kwargs):
        content = self.res_content(request.user)
        return Response(content, status=200)

    def put(self, request, format=None, **kwargs):
        serializer = serializers.UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            content = {
                "firstName": user.first_name,
                "lastName": user.last_name,
                "email": user.email
            }
            return Response(content, status=201)


class AddressView(APIView):

    def res_content(self, addresses):
        return {
            "addresses": [
                {
                    "id": a.id,
                    "flatNo": a.flat_no,
                    "street": a.street,
                    "area": a.area,
                    "locality": a.locality,
                } for a in addresses
            ]
        }

    def post(self, request, format=None, **kwargs):
        serializer = serializers.AddressSerializer(
            data=request.data,
            context={'user': request.user}
        )
        if serializer.is_valid():
            serializer.save()
            content = self.res_content(request.user.address_set.all())
            return Response(content, status=201)
        return Response(status=500)

    def put(self, request, format=None, id=None):
        serializer = serializers.AddressSerializer(
            request.user.address_set.get(id=int(id)),
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            content = self.res_content(request.user.address_set.all())
            return Response(content, status=201)
        return Response(status=500)

    def delete(self, request, format=None, id=None):
        address = request.user.address_set.get(id=int(id))
        address.delete()
        content = self.res_content(request.user.address_set.all())
        return Response(content, status=202)


#----------------------HOME---------------------------

class HomeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        content = {
            "notifications": {
                "load": True,
                "list": [
                    {
                        "title": n.title,
                        "body": n.body,
                        "updated": n.updated,
                        "seen": True
                    } for n in request.user.notification_set.all()[:20]
                ]
            },
            "topItems": [
                {
                    "id": i.id,
                    "name": i.name,
                    "price": i.price,
                    "img": {
                        "uri": i.img.url,
                        "name": i.img.name,
                    } if i.img else None,
                } for i in models.Item.objects.filter(top_product=True)
            ],
            "categories": [
                {
                    "id": c.id,
                    "name": c.name,
                    "img": {
                        "uri": c.img.url,
                        "name": c.img.name
                    } if c.img else None,
                } for c in models.Category.objects.all()
            ]
        }
        return Response(content, status=200)
        

#----------------------ITEMS--------------------------

def item_details_content(item):
    return {
        "id": item.id,
        "name": item.name,
        "price": item.price,
        "minimumOrder": item.minimum_order,
        "img": {
            "uri": item.img.url,
            "name": item.img.name,
        } if item.img else None,
        "description": item.description,
        "rating": item.ratingdetail_set.all().aggregate(Avg('stars'))['stars__avg'],
    }


class ItemsView(APIView):

    def get(self, request, format=None, category_id=None):
        category = models.Category.objects.get(id=int(category_id))
        content = {
            "items": {
                "CategoryId": category.id,
                "list": [
                    {
                        **item_details_content(i)
                    } for i in category.item_set.filter(status="active")
                ]
            }
        }
        return Response(content, status=200)


class ItemView(APIView):

    def res_content(self, item):
        return {
            "item": {
                **item_details_content(item)
            }
        }

    def get(self, request, format=None, item_id=None):
        item = models.Item.objects.get(id=int(item_id))
        content = self.res_content(item)
        return Response(content, status=200)

#----------------------CART---------------------------

def cart_item_detail(user):
    return {
        "addresses": [
            {
                "id": a.id,
                "flatNo": a.flat_no,
                "street": a.street,
                "area": a.area,
                "locality": a.locality,
            } for a in user.address_set.all()
        ],
        "cart": {
            "load": True,
            "products": [
                {
                    "id": o.id,
                    "items": [
                        {
                            **item_details_content(i),
                            "quantity": o.orderitem_set.get(item=i).quantity,
                            "orderItemId": o.orderitem_set.get(item=i).id,
                        } for i in o.items.all()
                    ]
                } for o in user.ordergroup_set.filter(status='cart')
            ]
        }
    }


class CartView(APIView):
    def get(self, request, format=None):
        content = cart_item_detail(request.user)
        return Response(content, status=200)


class CartCRUD(APIView):

    def put(self, request, format=None, item_id=None):
        item = models.Item.objects.get(id=int(item_id), status="active")
        try:
            order_group = request.user.ordergroup_set.get(
                status="cart"
            )
        except ObjectDoesNotExist:
            order_group = models.OrderGroup.objects.create(
                user=request.user,
                status="cart"
            )
        finally:
            if item not in order_group.items.all():
                models.OrderItem.objects.create(
                    order_group=order_group,
                    item=item,
                    quantity=item.minimum_order
                )
            content = cart_item_detail(request.user)
            return Response(content, status=201)

    def delete(self, request, format=None, item_id=None):
        order_item = models.OrderItem.objects.get(
            id=int(item_id),
            order_group__user=request.user
        )
        order_group = order_item.order_group
        if order_group.status == "cart":
            order_item.delete()
            if order_group.items.all().count() == 0:
                order_group.delete()
        content = cart_item_detail(request.user)
        return Response(content, status=202)


class CartItemCRUD(APIView):

    def put(self, request, format=None, id=None):
        order_item = models.OrderItem.objects.get(
            order_group__user=request.user,
            id=int(id)
        )
        quantity = int(request.data.get('quantity'))
        if quantity >= order_item.item.minimum_order:
            order_item.quantity = quantity
            order_item.save()
            content = cart_item_detail(request.user)
            return Response(content, status=201)
        return Response(status=500)

#----------------------ORDER---------------------------

def ordered_item_details(user):
    return {
        "orders": {
            "load": True,
            "products": [
                {
                    "id": o.id,
                    "status": o.status,
                    "items": [
                        {
                            **item_details_content(i),
                            "quantity": o.orderitem_set.get(item=i).quantity,
                            "orderItemId": o.orderitem_set.get(item=i).id,
                            "salePrice": o.orderitem_set.get(item=i).sale_price,
                        } for i in o.items.all()
                    ]
                } for o in user.ordergroup_set.filter(
                    ~Q(status="cancelled"), ~Q(status="cart"), ~Q(status="dropped")
                )
            ]
        }
    }


class PlaceOrderView(APIView):

    def put(self, request, format=None, cart_id=None):
        order_group = models.OrderGroup.objects.get(
            id=int(cart_id),
            user=request.user
        )
        inactive_items = order_group.orderitem_set.filter(~Q(item__status="active"))
        if inactive_items:
            item_names = ", ".join([i.item.name for i in inactive_items])
            return Response(
                {"message": f"{item_names} not available"},
                status=422
            )
        for oi in order_group.orderitem_set.all():
            oi.sale_price = oi.item.price
            oi.save()
        order_group.status = "ordered"
        order_group.amount = sum([
            item.price * item.orderitem_set.get(
                order_group=order_group
            ).quantity for item in order_group.items.all()
        ])
        order_group.address = request.user.address_set.get(
            id=int(request.data.get('addressId'))
        )        
        order_group.time = timezone.localtime()
        order_group.save()

        content = ordered_item_details(request.user)
        return Response(content, status=201)


class OrderList(APIView):
    def get(self, request, format=None):
        content = ordered_item_details(request.user)
        return Response(content, status=200)

#---------------------------AUTHANTICATION-------------------------------

def get_login(request, username, password):
    user = authenticate(username= username, password=password)
    if user is not None:
        login(request, user)
        return True
    else:
        return False


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        username = None
        phone= None
        email =None

        try:
            username = User.objects.get(username = data['username'])
        except:
            pass
        try:
            phone = models.CustomerPhone.objects.get(mobile = data['username'])
        except:
            pass
        try:
            email = User.objects.get(email= data['username'])
        except:
            pass

        if username is not None:
            user = get_login(request, username, data['password'])
            if user:
                return Response({'message':'User login'})
            else:
                return Response({'message':'Invalid User'})
        elif phone is not None:
            get_user = User.objects.get(username = phone.user)
            user = get_login(request, get_user.username, data['password'])
            if user:
                return Response({'message':'User login'})
            else:
                return Response({'message':'Invalid User'})
        elif email is not None:
            user = get_login(request, email.username, data['password'])
            if user:
                return Response({'message':'User login'})
            else:
                return Response({'message':'Invalid User'})
        else:
            return Response({'message':'Invalid User'})
            


class LogoutView(APIView):
    def get(self, request, format=None):
        logout(request)
        return Response(status=200)