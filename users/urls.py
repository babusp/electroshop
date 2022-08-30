from django.urls import path


from rest_framework_simplejwt.views import TokenRefreshView

from users.views import LoginAPIView, SignupAPIView, UpdateDeleteAPIView,ListAPIView



urlpatterns=[

    path("login/",LoginAPIView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view()),
    path('signup/',SignupAPIView.as_view()),
    path('list/',ListAPIView.as_view()),
    path('rudop/<int:pk>/',UpdateDeleteAPIView.as_view()),
    
]