from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .models import TelegramUser, Message
from .serializers import MessageSerializer


class UserRegistration(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        name = request.data.get('name')

        if not username or not password or not name:
            return Response({'error': 'Username, password and name are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = TelegramUser.objects.create_user(username=username, password=password, name=name)
        user.save()

        return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)


class UserLogin(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


class UserMessage(APIView):
    def post(self, request):
        message_text = request.data.get('message')
        user = request.user

        if not message_text and not user:
            return Response({'error': 'Message text and user is required'}, status=status.HTTP_400_BAD_REQUEST)

        Message(user=user, message_text=message_text).save()

        return Response({'message': f'Message sent successfully: {message_text}'}, status=status.HTTP_201_CREATED)


class AllUserMessages(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)
