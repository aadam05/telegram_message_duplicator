from django.urls import path
from .views import UserRegistration, UserLogin, UserMessage, AllUserMessages

app_name = 'factory_bot'

urlpatterns = [
    path('registration/', UserRegistration.as_view()),
    path('login/', UserLogin.as_view()),
    path('create_message/', UserMessage.as_view()),
    path('all_mesages/', AllUserMessages.as_view()),
]
