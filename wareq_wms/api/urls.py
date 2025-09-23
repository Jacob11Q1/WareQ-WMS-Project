from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CustomerViewSet, SupplierViewSet, ItemViewSet, OrderViewSet

# Router for CRUD endpoints
router = DefaultRouter()
router.register("customers", CustomerViewSet, basename="customers")
router.register("suppliers", SupplierViewSet, basename="suppliers")
router.register("items", ItemViewSet, basename="items")
router.register("orders", OrderViewSet, basename="orders")

urlpatterns = [
    # JWT Authentication
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # API Endpoints
    path("", include(router.urls)),
]
