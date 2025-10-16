from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from core.views import *

router = DefaultRouter()

router.register(r'categories', CategoryViewSet)
router.register(r'telephones', TelephoneViewSet)
router.register(r'addresses', AddressViewSet, basename='address')
router.register(r'naturalPersons', NaturalPersonViewSet)
router.register(r'restaurants', RestaurantViewSet)
router.register(r'recently-restaurant-views', RecentlyViewsViewSet, basename='recently-views')
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'marks', MarkViewSet)
router.register(r'colors', ColorViewSet)
router.register(r'products', ProductViewSet, basename='product')
router.register(r'favorites', FavoriteViewSet, basename='favorite')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'coupons', CouponViewSet)
router.register(r'coupons-client', CouponClientViewSet, basename='coupon-client')
router.register(r'restaurant-reviews', ReviewRestaurantViewSet)
router.register(r'response-restaurant-reviews', ResponseReviewRestaurantViewSet)
router.register(r'deliveryman-reviews', ReviewDeliverymanViewSet)
router.register(r'response-deliveryman-reviews', ResponseReviewDeliverymanViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # path('api/users/', include(usuario_router.urls)),
    path('api/user/', UserListAPIView.as_view()),
    path('api/user/register/', UserRegisterAPIView.as_view()),
    path('api/user/update/', UserUpdateAPIView.as_view()),
    path('api/user/register/google/', UserCreateByGoogleTokenAPIView.as_view(), 
    name="register_user_google"),
    path('api/user/login/google/', LoginByGoogleAPIView.as_view(), name="login_user_google"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]