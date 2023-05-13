from django.urls import path

# from .user_account import UserAccountViewSet
from . import user_account
from .user_profile import ProfileViewSet
from .department_and_position import DepartmentViewSet, PositionViewSet, OfficeViewSet
from .image_and_experience import ImageViewSet, SocailViewSet, ExperienceViewSet

from rest_framework.authtoken.views import ObtainAuthToken


urlpatterns = [
    path("user/login/", ObtainAuthToken.as_view(), name='api_token_auth'),
    path("user/signup/", user_account.signup_new_user, name='signup_new_user'),
    path("user/verify/", user_account.otp_verification, name='otp_verification'),
    path("user/", ProfileViewSet.as_view({
        'get' : 'user_details',
        'put' : 'update'
    }), name="user_account_manager"),

    path('profile/', ProfileViewSet.as_view({
        'get' : 'profile_details',
        'put' : 'update',
        'post' : 'create'
    }), name="user_profile_manager"),

    path('profile/<str:id>/', ProfileViewSet.as_view({
        'get' : 'profile_details',
    }), name="profile_details"),


    path('profile/experience/', ExperienceViewSet.as_view({
        'get' : 'all_experiences',
        'post' : 'create'
    }), name="experiene_manager"),

    path('profile/experience/<str:id>/', ExperienceViewSet.as_view({
        'put' : 'update',
    }), name="experiene_update"),

    path('profile/image/', ImageViewSet.as_view({
        'get' : 'all_images',
        'post' : 'create'
    }), name="image_manager"),

    path('profile/image/<str:id>/', ImageViewSet.as_view({
        'put' : 'update',
    }), name="image_update"),

    path('profile/social/', SocailViewSet.as_view({
        'get' : 'all_socails',
        'post' : 'create'
    }), name="social_manager"),

    path('profile/social/<str:id>/', SocailViewSet.as_view({
        'put' : 'update',
    }), name="social_update"),

    path('department/', DepartmentViewSet.as_view({
        'get' : 'all_departments',
        'post' : 'create',
    }), name="social_update"),

    path('position/', PositionViewSet.as_view({
        'get' : 'all_positions',
        'post' : 'create',
    }), name="social_update"),

    path('office/', OfficeViewSet.as_view({
        'get' : 'all_offices',
        'post' : 'create',
    }), name="social_update"),

]
