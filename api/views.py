from rest_framework import serializers
from django.contrib.auth import get_user_model # If used custom user model
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.core import exceptions
import django.contrib.auth.password_validation as validators

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        user = UserModel(**data)
        
        # get the password from the data
        password = data.get('password')
        
        errors = dict() 
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=user)
        
        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return super(UserSerializer, self).validate(data)

    def create(self, validated_data):

        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = UserModel
        # Tuple of serialized model fields (see link [2])
        fields = ( "id", "username", "password", )


class CreateUserView(CreateAPIView):

    model = get_user_model()
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer