from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BusinessUserCompletedOrderCountView, BusinessUserOrderCountView, OrderViewSet


router = DefaultRouter()
router.register(r"orders", OrderViewSet, basename="orders")


urlpatterns = [
    path("order-count/<int:business_user_id>/", BusinessUserOrderCountView.as_view(), name="business-user-order-count"),
    path("completed-order-count/<int:business_user_id>/", BusinessUserCompletedOrderCountView.as_view(), name="business-user-completed-order-count"),
    path("", include(router.urls)),
]
