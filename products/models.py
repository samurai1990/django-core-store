from core.base_model import BaseModel
from django.db import models
import time


def get_image_path(instance, filename):
    filename = filename.split('/')[-1]
    return "products/{0}_{1}_{2}".format(time.strftime("%Y%m%d"), instance.id, filename)


class Product(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.FileField(upload_to=get_image_path)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Product, self).delete(*args, **kwargs)

    class Meta:
        db_table = 'products'
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['-last_modified']
