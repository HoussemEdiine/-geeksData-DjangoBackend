from django.urls import path
from .views import RegisterUser, GetAllUsers , DeleteUser , UpdateUser , LoginUser , AddUser

urlpatterns = [
    path('register', RegisterUser.as_view()),
    path('users', GetAllUsers.as_view()),
    path('user/<str:pk>', DeleteUser.as_view()),
    path('updateuser/<str:pk>', UpdateUser.as_view()),
    path('login', LoginUser.as_view()),
    path('add' , AddUser.as_view() )
]
