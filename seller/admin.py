from django.contrib import admin
from .models import Item, Category, SellerPhone
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import ItemForm
from customer.models import OrderGroup, OrderItem, CustomerPhone, Address, RatingDetail

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 25



class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price','minimum_order','status']
    list_display_links = ['name', 'price','minimum_order',]
    search_fields = ['name', 'description']
    ordering = ('-price',)
    list_filter = ['price', 'status', 'category']
    list_per_page = 25
    list_editable = ['status',]
    readonly_fields = ['user']
    form = ItemForm

    '''
    def get_form(self, request, obj=None, **kwargs):
        form = super(ItemAdd, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        return form
    '''
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        try:
            obj.user = request.user
            obj.save()
        except:
            pass
        


class UserAdmin(BaseUserAdmin):
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_display = ('username', 'email', 'is_active', 'is_staff')
    list_editable = ['is_active']

    readonly_fields = [
        'last_login'
    ]
    fieldsets = (
        (None, {'fields': ('username', 'password')}) ,
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets =(
        ('Add user', {'fields': ('username', 'password1', 'password2', 'email')}) ,
    )
    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or (obj and obj.id == request.user.id)
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.id)
    

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(SellerPhone)
admin.site.register(Category, CategoryAdmin)
admin.site.register(OrderGroup)
admin.site.register(OrderItem)
admin.site.register(CustomerPhone)
admin.site.register(Address)
admin.site.register(RatingDetail)
