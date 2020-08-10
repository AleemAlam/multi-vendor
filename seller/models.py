from django.db import models
from django.contrib.auth.models import User


ITEM_STATUS = [
    ('offline', 'offline'),
    ('active', 'active')
]

class Category(models.Model):
    name = models.CharField(max_length=150)
    img = models.ImageField(upload_to="category_images/", blank=True, null=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Item(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, blank=True)
    name = models.CharField(max_length=150)
    price = models.IntegerField(default=0)
    minimum_order = models.IntegerField()
    img = models.ImageField(upload_to="item_images/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    top_product = models.BooleanField(default=False)
    status = models.CharField(max_length=25, choices=ITEM_STATUS, blank=True, null=True)

    def __str__(self):
        return self.name
