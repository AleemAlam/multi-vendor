from rest_framework import serializers
from django.contrib.auth.models import User
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        exclude = ['user']

    def create(self, validated_data):
        address = models.Address.objects.create(
            user=self.context.get('user'),
            **validated_data
        )
        return address

    def update(self, instance, validated_data):
        instance.flat_no = validated_data.get('flat_no', instance.flat_no)
        instance.street = validated_data.get('street', instance.street)
        instance.area = validated_data.get('area', instance.area)
        instance.locality = validated_data.get('locality', instance.locality)
        instance.save()
        return instance