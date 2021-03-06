from django.urls import path, include
from .views import (ExampleAuthentication, UserViewSet, UserProfileViewSet,
                    GroupViewSet, ProductViewSet, OrderViewSet
                    )
from rest_framework import routers

# import rest_auth
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profile', UserProfileViewSet)
router.register(r'product', ProductViewSet)
router.register(r'order', OrderViewSet)
# router.register(r'groups', GroupViewSet)

# app_name="user-api"
urlpatterns = [
    path('', include(router.urls)),
    path('rest-auth/', include('rest_auth.urls')),
    #  path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api-token-auth/', ExampleAuthentication.as_view())
]
