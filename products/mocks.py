from .models import Product
from django.core.files import File as DjangoFile


def _get_sample_product_data(name=None, description=None, image_path=None):
    data = {
        'name': "iphone" if name is None else name,
        'description': "mobile device" if description is None else description,
        'image': DjangoFile(open(file='products/test_cases/test.jpg', mode='rb')) if image_path is None else DjangoFile(open(file=image_path, mode='rb')),
    }
    return data


def get_sample_product_data(name=None, description=None, image_path=None):
    data = _get_sample_product_data(
        name=name, description=description, image_path=image_path)
    return data


def get_sample_product_model(name=None, description=None, image_path=None):
    data = _get_sample_product_data(
        name=name, description=description, image_path=image_path)
    return Product.objects.create(**data)
