from django.urls import path
from .views import PageInfoView

urlpatterns = [
    path('base-info/', PageInfoView.as_view(), name="page-statistics"),
]