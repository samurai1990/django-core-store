from django.test import TestCase
from .mocks import get_sample_product_data, get_sample_product_model
from accounts.tests import BaseAuthTestCase
from accounts.mocks import get_sample_superuser_with_password
from django.urls import reverse


class TargetTestCase(TestCase):
    databases = {'default'}

    def test_create_product(self):
        Target = get_sample_product_model()
        self.assertIsNotNone(Target)


class TargetAPITestCase(BaseAuthTestCase):
    databases = {'default'}

    def setUp(self):
        self.user, self.password = get_sample_superuser_with_password()

    def _create_sample_Target(self):
        for i in range(2):
            if i % 2 == 0:
                get_sample_product_model(name="ipad")
            else:
                get_sample_product_model()

    def test_create_Target(self):
        self.auth(self.user.username, self.password)
        url = reverse('product-list')
        data = get_sample_product_data()
        response = self.client.post(path=url, data=data, format='multipart')
        self.check_create_status_code(response)
        self.check_body_ok_errors(response)
        self.assertIsNotNone(response.json().get('data').get('product'))
        return response.json().get('data').get('product')

    def test_partial_update_as(self):
        Target = self.test_create_Target()
        url = reverse('product-detail', args={Target.get('id')})
        data = {'ip': '127.0.0.1'}
        response = self.client.patch(path=url, data=data, format='multipart')
        self.check_ok_status_code(response)
        self.check_body_ok_errors(response)
        self.assertEqual(response.json().get('data').get(
            'product').get('port'), data.get('port'))

    def test_retrieve_Target(self):
        Target = self.test_create_Target()
        url = reverse('product-detail', args={Target.get('id')})
        response = self.client.get(path=url)
        self.check_ok_status_code(response)
        self.check_body_ok_errors(response)

    def test_list_Target(self):
        self._create_sample_Target()
        self.auth(self.user.username, self.password)
        url = reverse('product-list')
        response = self.client.get(path=url)
        self.check_ok_status_code(response)
        self.check_body_ok_errors(response)
        self.assertEqual(
            len(response.json().get('data').get('products')), 2)

    def test_delete_Target(self):
        Target = self.test_create_Target()
        url = reverse('product-detail', args={Target.get('id')})
        response = self.client.delete(path=url)
        self.check_no_content_status_code(response)
