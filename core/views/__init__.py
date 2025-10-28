from .user import UserRegisterAPIView, CodeAPIView, UserListAPIView, UserUpdateAPIView
from .google import UserCreateByGoogleTokenAPIView, LoginByGoogleAPIView
from .category import CategoryViewSet
from .telephone import TelephoneViewSet
from .address import AddressViewSet
from .natural_person import NaturalPersonViewSet
from .restaurant import RestaurantViewSet, RecentlyViewsViewSet
from .vehicle import VehicleViewSet
from .mark import MarkViewSet
from .color import ColorViewSet
from .product import ProductViewSet
from .favorite import FavoriteViewSet
from .order import OrderViewSet, ProductOrderViewSet
from .payment import PaymentViewSet
from .coupon import CouponViewSet, CouponClientViewSet, CouponClientOrderViewSet
from .review_restaurant import ReviewRestaurantViewSet, ResponseReviewRestaurantViewSet
from .review_deliveryman import ReviewDeliverymanViewSet, ResponseReviewDeliverymanViewSet