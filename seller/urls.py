from django.urls import path
from . import views
from . import api_view

urlpatterns = [
    path('create/seller/', api_view.SellerCreateView.as_view(), name = 'create_seller'),
]