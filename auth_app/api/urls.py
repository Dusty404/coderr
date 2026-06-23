from django.urls import path
from .views import RegistrationView, CustomLoginView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name="login"),
    path('registration/', RegistrationView.as_view(), name="registration"),
]