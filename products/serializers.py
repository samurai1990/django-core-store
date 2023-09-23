from rest_framework import serializers
from .models import Product


class ProductCreateRequest(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Product


class ProductCreateResponse(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'description', 'image']
        model = Product


class ProductListResponse(ProductCreateResponse):
    class Meta(ProductCreateResponse.Meta):
        pass


class ProductRetrieveResponse(ProductCreateResponse):
    class Meta(ProductCreateResponse.Meta):
        pass


class ProductUpdateRequest(ProductCreateRequest):
    class Meta(ProductCreateRequest.Meta):
        pass


class ProductUpdateResponse(ProductCreateResponse):
    class Meta(ProductCreateResponse.Meta):
        pass
