from .user import UserRegisterSerializer
from .category import CategorySerializer
from .telephone import TelephoneSerializer
from .address import AddressSerializer
from .natural_person import NaturalPersonSerializer
from .restaurant import RestaurantSerializer
from .vehicle import VehicleSerializer
from .mark import MarkSerializer
from .color import ColorSerializer
from .product import ProductSerializer
from .favorite import FavoriteSerializer
from .order import OrderListSerializer, OrderRetrieveSerializer, CreateOrderSerializer, DeliveryManAcceptOrderSerializer, ProductOrderSerializer
from .coupon import CouponSerializer, CouponClientSerializer, CouponClientOrderSerializer