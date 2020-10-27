from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import User, Book
from .serializers import UserSerializer, BookSerializer
from .permissions import HasActiveSubscription


class UserList(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


class UserInfo(generics.RetrieveAPIView):
    queryset = User.objects.select_related("subscriptions", "subscriptions__subscription")
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class BookList(generics.ListCreateAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.all()


class BookInfo(generics.RetrieveAPIView):
    queryset = Book.objects
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HasActiveSubscription]

