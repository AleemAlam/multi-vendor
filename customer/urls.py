from django.urls import path
from . import views
from . import api_view

urlpatterns = [

    # CUSTOMER
    path('create/', api_view.CustomerCreateView.as_view(), name = 'create_customer'),
    path('validate/', api_view.ValidateOTP.as_view(), name = 'validate_otp_customer'),
    path('resend/otp/', api_view.ResendOTP.as_view(), name = 'resend_otp_customer'),
    path('update/number/', api_view.UpdateNumber.as_view(), name = 'update_number_customer'),
    path('user/profile/', api_view.ProfileView.as_view(), name = 'profile_customer'),
    path('user/address/', api_view.AddressView.as_view(), name = 'address_customer'),

    # AUTHENTICATION
    path('login/', api_view.LoginView.as_view(), name = 'login_customer'),
    path('logout/', api_view.LogoutView.as_view(), name = 'logout_customer'),

    # HOME
    path('home/', api_view.HomeView.as_view(), name = 'home_customer'),

    # ITEMS
    path('items/all/<int:category_id>/', api_view.ItemsView.as_view(), name = 'all_items_coustomer'),
    path('item/<int:item_id>/', api_view.ItemView.as_view(), name = 'item_customer'),

    # CART
    path('cart/view/', api_view.CartView.as_view(), name = 'cart_customer'),
    path('cart/<int:item_id>/', api_view.CartCRUD.as_view(), name = 'cart_crud_customer'),
    path('cart/item/<int:id>/', api_view.CartItemCRUD.as_view(), name = 'cart_item_customer'),

    # ORDER
    path('order/place/<int:cart_id>/', api_view.PlaceOrderView.as_view(), name = 'place_order_customer'),
    path('order/list/', api_view.OrderList.as_view(), name = 'order_list_customer'),
]