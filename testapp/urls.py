from django.urls import path

from testapp.views import UserProfileAPIView,sendotpview

urlpatterns=[

    path("profile/",UserProfileAPIView.as_view()),
    path("otp",sendotpview.as_view()),
]
