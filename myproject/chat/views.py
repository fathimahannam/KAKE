from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import viewsets
from .models import Message
from .serializers import MessageSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from app.models import *
from app.serializers import *

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()



    @action(detail=False, methods=['post'])
    def send_message(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)





@api_view(['GET'])
def get_messages(request, user_id, mentor_id):
    try:

        sender = get_object_or_404(UserAccount, id=user_id)

        receiver = get_object_or_404(UserAccount, id=mentor_id)

        messages = Message.objects.filter(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(f"An error occurred: {e}")
        return Response({"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_mentor_users(request, mentor_id):
    mentor = get_object_or_404(get_user_model(), id=mentor_id)
    
    # Get users who have sent or received messages from the mentor
    users = get_user_model().objects.filter(
        Q(sent_messages__receiver=mentor) | Q(received_messages__sender=mentor)
    ).distinct()

    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
