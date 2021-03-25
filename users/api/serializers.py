from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.contrib.auth import get_user_model
# from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import LoginSerializer
# Serializers define the API representation.
from users.models import UserProfile, Product, Order
USER = get_user_model()


# class CustomRegisterSerializer(RegisterSerializer):
#     """
#     Custom User Registeration Serializer Inhereting from rest_auth RegisterSerializer
#     """
#     # email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
#     email = None


class CustomLoginSerializer(LoginSerializer):
    """
    Custom User Login Serializer Inhereting from rest_auth LoginSerializer

    """
    # renderer_classes = [JSONRenderer]
    # email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)

    # def validate(self, attrs):
    #     attrs = super(CustomLoginSerializer, self).validate(attrs)
    #     print(attrs)
    #     return attrs
    # print(self.data())

    # def data(self, *args, **kwargs):
    #     data = super().data(*args, **kwargs)
    #     print(data)
    #     return data
    def get_serializer_context(self, *args, **kwargs):
        context = super(CustomLoginSerializer).get_serializer_context(
            *args, **kwargs)

        print(context)
        context['message'] = 'No Message'
        # context.update({"request": self.request})
        return context

    email = None


class ListAllUserSerializer(serializers.ModelSerializer):
    '''
    Show all users list
    '''
    class Meta:
        model = USER
        fields = ['id', 'username', 'date_joined']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """ Show Group attached with a url"""
    class Meta:
        model = Group
        fields = ['url', 'name']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """ Show User attached with a url"""
    class Meta:
        model = USER
        fields = ['url', 'username', 'name',
                  'email', 'password', 'last_login', ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = USER(email=validated_data['email'],
                    name=validated_data['name'],
                    username=validated_data['username']
                    )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    """ Show userProfile attached with a url"""
    class Meta:
        model = UserProfile
        fields = ['url', 'user', 'image', ]


class UserDetailSerializer(serializers.ModelSerializer):
    """ Show User Detail Serializer"""
    class Meta:
        model = USER
        fields = [
            'username',
            'email',
            'last_login',
        ]


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """ Show Product attached with a url"""

    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """ Show Order attached with a url"""

    class Meta:
        model = Order
        fields = '__all__'
