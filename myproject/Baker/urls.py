from django.urls import path
from . import views
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('', views.get_bakers, name='get_bakers'),
    path('baker-application/', views.baker_application_view, name='baker-application'),
    path('view-bakers/', views.view_bakers, name='view_bakers'),
    path('view-staff/', views.get_staff, name='view_bakers'),
    path('view-baker-requests/', views.view_baker_requests, name='view_baker_requests'),
    path('approve/<int:baker_id>/', views.approve_baker_request, name='approve_baker_request'),
    path('reject/<int:baker_id>/', views.reject_baker_request, name='reject_baker_request'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile-detail'),
    path('api/baker/<int:pk>/', views.BakerDetailView.as_view(), name='baker-detail'),
    path('cakes/', views.cake_application_view.as_view()),
    path('show-cakes/', views.user_cakes, name='user_cakes'),
    
    path('cakess/<int:pk>/', CakeDetail.as_view(), name='cake-detail'),
    path('user-profiles/<int:user_id>/', views.user_profile_api, name='user-profile-api'),
    path('show-cakes/<int:user_id>/', views.get_user_cakes, name='get_user_cakes'),
    path('api/add-to-wishlist/<int:cake_id>/', views.AddToWishlistView.as_view(), name='add_to_wishlist_api'),
    path('api/remove-from-wishlist/<int:pk>/', views.RemoveFromWishlistView.as_view(), name='remove_from_wishlist_api'),
    path('wishlist/', views.WishlistListView.as_view(), name='wishlist-list'),
    path('editbakers/<int:user_id>/', views.BakerProfileView.as_view(), name='baker_profile'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('get_orders/<int:user_id>/', get_orders, name='api_user_orders'),
    path('baker/<int:baker_id>/orders/', baker_orders, name='baker_orders'),
    path('baker/<int:baker_id>/orders/<int:order_id>/update-status/', OrderStatusView.as_view(), name='update_order_status'),
   

]
