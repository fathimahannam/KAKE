# views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.http import require_http_methods
from app.serializers import UserSerializer
from .models import Baker
from .serializers import BakerApplicationSerializer, BakerSerializer
from rest_framework import generics
from rest_framework.views import APIView 
from .models import *
from .serializers import *
from rest_framework import generics, permissions

from .serializers import UserProfileSerializer
from rest_framework.parsers import MultiPartParser, FormParser
@api_view(['POST'])
def create_baker(request):
    if request.method == 'POST':
        serializer = BakerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(is_active=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_bakers(request):
    bakers = Baker.objects.filter(is_active=True)
    baker_data = [
        {
            'name': baker.name,
            'image_url': baker.image.url,
        }
        for baker in bakers
    ]
    return JsonResponse({'bakers': baker_data})

@api_view(['POST'])
def baker_application_view(request):
    if request.method == 'POST':
        print(request.data)
        serializer = BakerApplicationSerializer(data=request.data)
        
        if serializer.is_valid():
            print('asdasd',serializer.errors)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def view_bakers(request):
    bakers = Baker.objects.filter(is_active=True)
    serialized_bakers = BakerWithUserIdSerializer(bakers, many=True)
    return Response(serialized_bakers.data)

@api_view(['GET'])
def view_baker_requests(request):
    bakers = Baker.objects.filter(is_active=False)
    serialized_baker_requests = BakerApplicationSerializer(bakers, many=True)
    return Response(serialized_baker_requests.data)

@api_view(['GET'])
def get_staff(request):
    users = UserAccount.objects.filter(is_staff=True)  
    serialized_users = UserSerializer(users, many=True)
    return Response(serialized_users.data)

@api_view(['POST'])
def approve_baker_request(request, baker_id):
    baker = get_object_or_404(Baker, id=baker_id)
    user = baker.user
    user.is_staff = True
    user.save()
    baker.is_active = True
    baker.save()
    return Response({'message': 'Baker request approved successfully'})

@api_view(['POST'])
def reject_baker_request(request, baker_id):
    baker = get_object_or_404(Baker, id=baker_id)
    baker.delete()
    return Response({'message': 'Baker request rejected and baker deleted successfully'},status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user_data = UserProfileSerializer(instance).data

     
        image_urls = [instance.image.url] if instance.image else []

        response_data = {
            'user_data': user_data,
            'image_urls': image_urls,
        }

        return Response(response_data)
    
class BakerDetailView(generics.RetrieveAPIView):
    queryset = Baker.objects.all()
    serializer_class = BakerSerializer



class cake_application_view(generics.CreateAPIView):
    queryset = Cake.objects.all()
    serializer_class = CakeSerializer

@api_view(['GET'])
def user_cakes(request):
    user_id = request.query_params.get('user_id')
    
    if user_id is not None:
        cakes = Cake.objects.filter(user_id=user_id)
        serializer = CakeSerializer(cakes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error': 'user_id parameter is missing'}, status=400)



    
@api_view(['GET'])
def user_profile_api(request, user_id):
    try:
        # Retrieve the user profile based on the provided user_id
        user_profile = Baker.objects.get(user__id=user_id)

        serializer = BakerSerializer(user_profile)

        return JsonResponse(serializer.data)
    except UserProfile.DoesNotExist:
         # Handle the case where the user profile is not found
        return JsonResponse({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)

def  get_user_cakes(request, user_id):
    cakes = Cake.objects.filter(user_id=user_id)
    print("Number of cakes found:", len(cakes)) 
    cake_data = []

    for cake in cakes:
        cake_data.append({
            'cakeName': cake.cakeName,
            'description': cake.description,
            'price': str(cake.price),
            'availableSizes': cake.availableSizes,
            'flavors': cake.flavors,
            'image_url': cake.image.url,
            'created_at': cake.created_at.isoformat()
        })

    return JsonResponse(cake_data, safe=False)

from rest_framework import viewsets
from .models import Cake
from .serializers import CakeSerializer

class CakeDetail(generics.RetrieveAPIView):
    queryset = Cake.objects.all()
    serializer_class = CakeSerializer

class CakeViewSet(viewsets.ModelViewSet):
    queryset = Cake.objects.all()
    serializer_class = CakeSerializer


class WishlistListView(generics.ListAPIView):
    serializer_class = WishlistSerializer
  

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)


class AddToWishlistView(generics.CreateAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
   

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RemoveFromWishlistView(generics.DestroyAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer


class WishlistListView(generics.ListCreateAPIView):
    serializer_class = WishlistSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)
    

class BakerProfileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, user_id):
        # Find the Baker instance related to the UserAccount by user_id
        baker = get_object_or_404(Baker, user_id=user_id)
        serializer = BakerSerializer(baker)
        return Response(serializer.data)

    def put(self, request, user_id):
        # Find the Baker instance related to the UserAccount by user_id
        baker = get_object_or_404(Baker, user_id=user_id)
        serializer = BakerSerializer(baker, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(BakerSerializer(baker).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    
@api_view(['GET'])
def user_orders(request, user_id):
    try:
        user_orders = Order.objects.filter(user__id=user_id)
        serializer = OrderSerializer(user_orders, many=True)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    


@api_view(['GET'])
def get_orders(request, user_id):
    try:
        user_orders = Order.objects.filter(user__id=user_id)
        serializer = OrderSerializer(user_orders, many=True)

        return JsonResponse(serializer.data, safe=False)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'User orders not found'}, status=status.HTTP_404_NOT_FOUND)
    

def baker_orders(request, baker_id):
    baker = get_object_or_404(UserAccount, id=baker_id)
    orders = Order.objects.filter(product__user=baker)
    serializer = OrderSerializer(orders, many=True)

    data = [
        {
            'order_id': order.id,
            'user': order.user.id,
            'cake': order.product.cakeName,
            'status': order.status,
            'price': order.product.price,
            'address': order.address,
            'datetime': order.datetime,
        }
        for order in orders
    ]

    return JsonResponse({'orders': data})


class OrderStatusView(APIView):
    def patch(self, request, baker_id, order_id):
        print("The baker_id: ", baker_id)
        print("The order_id: ", order_id)

        if request.method == 'PATCH':
            new_status_data = request.data.get('status')
            
            # Check if new_status_data is a dictionary with 'undefined' key
            if isinstance(new_status_data, dict) and 'undefined' in new_status_data:
                # Extract the value associated with 'undefined' key
                new_status = new_status_data['undefined']
            else:
                # If 'status' is not a dictionary, use it directly
                new_status = new_status_data
            
            print(new_status, "=========")
            
            
            order = get_object_or_404(Order, id=order_id)
            print(order)
            order.status = new_status
            order.save()
            return JsonResponse({'message': 'Status updated successfully'})
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=400)

