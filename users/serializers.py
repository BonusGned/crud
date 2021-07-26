from rest_framework import serializers, exceptions
from django.contrib.auth import password_validation
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'date_joined')

    def validate_password(self, password):
        password_validation.validate_password(password, self.instance)
        return password

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))
        instance.save()

        return instance
