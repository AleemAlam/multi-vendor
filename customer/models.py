from django.db import models
from django.contrib.auth.models import User
from seller.models import Item, Category
from decimal import Decimal
from django.core.validators import RegexValidator


ORDER_STATUS = [
    ('Cart', 'cart'),
    ('Cancelled', 'cancelled'),
    ('Ordered', 'ordered'),
    ('Received', 'received'),
    ('Ready to dispatch', 'ready to dispatch'),
    ('Dispatched', 'dispatched'),
    ('Delivered', 'delivered'),
    ('Dropped', 'dropped'),
]

class CustomerPhone(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.mobile)


class PhoneOTP(models.Model):
    phone_number_expretion = RegexValidator( regex=r'^\+?1?\d{9,14}$', message="Phone Number must be Entered in the format: '+9999999999', Upto 14 digits" )
    mobile = models.CharField(validators=[phone_number_expretion], max_length=15,)
    otp = models.CharField(max_length=4, blank=True, null=True)

    def __str__(self):
        return self.phone_number + ' is send '+ self.otp


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flat_no = models.CharField(max_length=20)
    street = models.CharField(max_length=20)
    area = models.CharField(max_length=20)
    locality = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.flat_no}, {self.street}, {self.area}, {self.locality}'

    def full_address(self):
        return f'{self.flat_no}, {self.street}, {self.area}, {self.locality}'


class RatingDetail(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(default=1)
    text = models.TextField(blank=True)


class OrderGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through="orderitem")
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        blank=True,
        null=True
    )
    status = models.CharField(max_length=150, choices=ORDER_STATUS)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return self.user.first_name


class Invoice(models.Model):
    order_group = models.OneToOneField(OrderGroup, on_delete=models.CASCADE)
    file = models.FileField(upload_to='invoices/', default='sample.pdf')
    generated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_group.user.username


class OrderItem(models.Model):
    order_group = models.ForeignKey(OrderGroup, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    sale_price = models.IntegerField(
        default=0,
        help_text="Amount (INR) in numbers, Do not use any symbols or text"
    )
    quantity = models.IntegerField()

    def __str__(self):
        return self.item.name


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    body = models.TextField(blank=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated']