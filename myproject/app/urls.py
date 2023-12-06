from django.urls import path
from . import views
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
    
    path('signup/', views.UserRegistration.as_view(),name='signup'),
    path('api/get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),
    path('', views.getRoutes, name='get_routes'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('activate/<uidb64>/<token> ', views.Activate, name='activate'),
    path('users/<int:user_id>/', views.get_user_info, name='get_user_info'),
    path('users/',views.get_users,name='get-users'),
    path('add-address/', views.add_address, name='add_address'),
    # path('get-addresses/', views.get_addresses, name='get_addresses'),

    path('existing-addresses/<int:user_id>/', get_address, name='api_user_orders'),

    path("create/<int:user_id>/",CreateOrderAPIView.as_view(), name="create-order-api"),
    path("complete/<int:user_id>/",views.TransactionAPIView, name="complete-order-api"),


]