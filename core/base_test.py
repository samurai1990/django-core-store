from rest_framework.test import APITestCase
from rest_framework import status
from . import errors


class BaseAPITestCase(APITestCase):
    def check_create_status_code(self, response):
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def check_ok_status_code(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def check_no_content_status_code(self, response):
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def check_reset_content_status_code(self, response):
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def check_body_ok_errors(self, response):
        self.assertEqual(response.json().get('err'), False)
        self.assertEqual(response.json().get(
            'err_code'), errors.ERR_SUCCESSFUL)
