from core.base_viewset import BaseViewSet
from accounts.permissions import IsAdmin
from . import serializers as ser
from .models import Product


class ProductViewSet(BaseViewSet):
    queryset = Product.objects.all()
    serializer_action_classes = {
        'create': {
            'req': ser.ProductCreateRequest,
            'res': ser.ProductCreateResponse,
        },
        'update': {
            'req': ser.ProductUpdateRequest,
            'res': ser.ProductUpdateResponse
        },
        'partial_update': {
            'req': ser.ProductUpdateRequest,
            'res': ser.ProductUpdateResponse
        },
        'retrieve': {
            'res': ser.ProductRetrieveResponse
        },
        'list': {
            'res': ser.ProductListResponse,
        },
    }
    permission_action_classes = {
        'create': [IsAdmin, ],
        'update': [IsAdmin, ],
        'partial_update': [IsAdmin, ],
        'retrieve': [IsAdmin, ],
        'list': [IsAdmin, ],
    }