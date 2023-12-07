from django.conf import settings
from django.shortcuts import render
from django.middleware.csrf import get_token
from django.core.mail import send_mail
# Create your views here.
from rest_framework import status
from django.shortcuts import render,redirect
from django.contrib.auth import logout
from .import client
from rest_framework.serializers import ValidationError
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import api_view
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['is_admin']=user.is_admin
        token['is_staff']=user.is_staff

        


        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer 

@api_view(["GET"])
def getRoutes(request):
    routes = [
        "api/login",
    ]
    return Response(routes)

class UserRegistration(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        serializer = UserRegisterSerializer(data=request.data)
        print("seriiiiiiiiiiiiiiiiiiiiiiiiiii",serializer)
     
        if serializer.is_valid(raise_exception=True):

            user = serializer.save()
            user.set_password(password)
           
            print("userrrrrrrrrrrrrrrrrrrrrrr", user)
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('account_verification.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'cite': current_site
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return Response({'status': 'success', 'msg': 'A verificaiton link sent to your registered email address', "data": serializer.data})
        else:
            return Response({'status': 'error', 'msg': serializer.errors})

@api_view(['GET'])
def Activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserAccount._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserAccount.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        print('User activated successfully.')
        return HttpResponseRedirect('https://kake-frontend-25veqpkl9-hannas-projects-70800ae4.vercel.app/login')
    else:
        # Return a response indicating that activation failed
        return Response({'message': 'Activation failed'}, status=status.HTTP_400_BAD_REQUEST)
    
    
def get_user_info(request, user_id):
    
    user = get_object_or_404(UserAccount, id=user_id)

    
    user_data = {
        'name': user.name, 
        'email': user.email, 
        
        
    }

   
    return JsonResponse(user_data)


def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrf_token': token})

@api_view(['GET'])
def get_users(request):
    users=UserAccount.objects.filter(is_admin=False)
    serilaized_users = UserSerializer(users,many=True)
    return Response(serilaized_users.data)
#address----------------------

@api_view(['GET'])
def get_address(request, user_id):

    user_address = Address.objects.filter(user__id=user_id)
    serializer = UserAddressSerializer(user_address, many=True)

    return JsonResponse(serializer.data, safe=False)

    return JsonResponse({'error': 'User orders not found'}, status=status.HTTP_404_NOT_FOUND)

    
@api_view(['POST'])
def add_address(request):
    if request.method == 'POST':
        address = request.data.get('address')
        user_id = request.data.get('user')  # Ensure that 'user' contains the user ID

        if address and user_id:
            # Retrieve the user account based on the user ID
            user = UserAccount.objects.get(id=user_id)
            # Create a new address associated with the user
            new_address = Address(user=user, address=address)
            new_address.save()
            return Response({'message': 'Address added successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Address and user fields are required.'}, status=status.HTTP_400_BAD_REQUEST)


def get_existing_addresses(request, user_id):
    print("======================")

    if request.method == 'GET':
        print("======================")
        addresses = Address.objects.filter(user_id=user_id)
        existing_addresses = [address.address for address in addresses]
        print("======================")

        return JsonResponse({'existing_addresses': existing_addresses})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
    
from django.shortcuts import get_object_or_404, render
from django.views import View
from .import client
from rest_framework.serializers import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import razorpay
# Create your views here.

class RazorpayClient:

    def create_order(self,amount,currency):
        print("================")
        data = {
            "amount" : amount * 100,
            "currency" : currency,
        }
        try:
            order_data = client.order.create(data=data)
            print(order_data,"=========++++++++++++")  
            return order_data
        except Exception as e:
            raise ValidationError(
                {
                    "status_code" : status.HTTP_400_BAD_REQUEST,
                    "message" : e
                }
            )
    
    def verify_payment(self, razorpay_order_id, razorpay_payment_id, razorpay_signature):
        try:
            return client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
        except Exception as e:
            raise ValidationError(
                {
                    "status_code" : status.HTTP_400_BAD_REQUEST,
                    "message" : e
                }
            )


rz_client = RazorpayClient


class CreateOrderAPIView(APIView):
    def post(self, request, user_id):
       
        user = get_object_or_404(UserAccount, id=user_id)
        create_order_serializer = CreateOrderSerializer(data=request.data)
        if create_order_serializer.is_valid():
            print(create_order_serializer)
            rz_client_instance = RazorpayClient()  
            order_response = rz_client_instance.create_order(
                amount=create_order_serializer.validated_data.get("amount"),
                currency=create_order_serializer.validated_data.get("currency")
            )
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "order created",
                "data": order_response
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad requesttt",
                "error": create_order_serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        



@api_view(['POST'])
def TransactionAPIView(request,user_id):
    if request.method == 'POST':
        user = get_object_or_404(UserAccount, id=user_id)
        transaction_serializer = TransactionModelSerializer(data=request.data)
        print(user_id,'daxo')
        print(transaction_serializer)
        if transaction_serializer.is_valid():
            
            rz_client = razorpay.Client(auth=("rzp_test_tgCvOVZCwscP6c", "W2YofbbI4LVREfIAlPtqti6U"))

            
            try:
                rz_client.utility.verify_payment_signature({
                    "razorpay_signature": transaction_serializer.validated_data.get("signature"),
                    "razorpay_payment_id": transaction_serializer.validated_data.get("payment_id"),
                    "razorpay_order_id": transaction_serializer.validated_data.get("order_id"),
                })
            except Exception as e:
                return JsonResponse({
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "error": str(e)
                }, status=status.HTTP_400_BAD_REQUEST)

            # Save the transaction and update user status
            transaction_serializer.save(user=user)
            subject = 'order placed'
            message = 'new order has been placed. .'
            from_email = 'verbvoyage2023@gmail.com'
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list)
            
            return JsonResponse({
                "status_code": status.HTTP_201_CREATED,
                "message": "transaction created"
            }, status=status.HTTP_201_CREATED)
        else:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "error": transaction_serializer.errors
            }
            return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)