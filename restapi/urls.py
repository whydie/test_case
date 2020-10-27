from django.urls import path

from .views import UserList, UserInfo, BookList, BookInfo
from .webhooks import payment_processed


urlpatterns = [
    path('user/', UserList.as_view(), name="user_list"),
    path('user/<int:pk>/', UserInfo.as_view(), name="user_info"),

    path('book/', BookList.as_view(), name="book_list"),
    path('book/<int:pk>/', BookInfo.as_view(), name="book_info"),

    path('payment/', payment_processed, name="payment")
]


