from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import OfferDetailViewSet, OffersViewSet


router = DefaultRouter()
router.register(r"offers", OffersViewSet, basename="offers")
router.register(r"offerdetails", OfferDetailViewSet, basename="offerdetails")

urlpatterns = [
    path("", include(router.urls)),
]
