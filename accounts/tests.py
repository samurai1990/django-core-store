from datetime import timedelta
from django.urls import reverse
from django.test import TestCase
from core.base_test import BaseAPITestCase
from rest_framework import status
from core import errors
from .models import User
from .mocks import get_sample_user


class BaseAuthTestCase(BaseAPITestCase):
    def cred_login(self, username, password):
        data = {
            'username': username,
            'password': password,
        }
        url = reverse('user-signin')
        response = self.client.post(path=url, data=data, format='json')
        return response

    def auth(self, username, password, api_key=None):
        res = self.cred_login(username, password)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json().get('err'), False)
        self.assertEqual(res.json().get('err_code'), errors.ERR_SUCCESSFUL)
        access_token = res.json().get('data').get('user').get('access_token')
        if api_key is not None:
            access_key = res.json().get('data').get('user').get('profile').get('api_token')
            self.assertIsNotNone(access_key)
            self.client.credentials(HTTP_API_KEY=access_key)
        else:
            self.assertIsNotNone(access_token)
            self.client.credentials(
                HTTP_AUTHORIZATION=f'token {access_token}')


class UserModelTestCase(TestCase):
    def setUp(self):
        pass

    def test_create_normal_user(self):
        normal_user = User.objects.create(
            username='normal', email='normal@example.com', password='normal')
        self.assertIsNotNone(normal_user)
        self.assertIsNotNone(normal_user.profile)
        self.assertIsNotNone(normal_user.profile.api_token)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            username='superuser',
            email='superuser@example.com',
            password='superuser')
        self.assertIsNotNone(superuser)
        self.assertIsNotNone(superuser.profile)

    def test_delete_user(self):
        user = User.objects.create(
            username='user',
            email='user@exmaple.com',
            password='password')
        user.delete()
        deleted_user = User.allobjects.get(id=user.id)
        self.assertEqual(deleted_user.is_deleted, True)
        self.assertEqual(deleted_user.is_active, False)


class UserViewSetTestCase(BaseAuthTestCase):
    def setUp(self):
        self.dup_data = {
            'username': 'duplicateuser',
            'password': 'duplicateuser',
            'email': 'duplicateuser@example.com',
        }
        self.dupuser = User.objects.create(**self.dup_data)
        self.sup_data = {
            'username': 'superteuser',
            'password': 'superteuser',
            'email': 'superuser@example.com',
        }
        self.supuser = User.objects.create_superuser(**self.sup_data)

    def _create_sample_users(self):
        for i in range(25):
            if i % 2 == 0:
                get_sample_user(
                    username=f'testuser{i}', password=f'testuser{i}', email=f'testuser{i}@example.com', superuser=True)
            else:
                get_sample_user(
                    username=f'testuser{i}', password=f'testuser{i}', email=f'testuser{i}@example.com', active=False,)

    def test_create_user(self):
        url = reverse('user-list')
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com'
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get('err'), False)
        self.assertEqual(response.json().get(
            'err_code'), errors.ERR_SUCCESSFUL)
        self.assertIsNotNone(response.json().get(
            'data').get('user').get('access_token'))
        self.assertIsNotNone(response.json().get('data').get(
            'user').get('profile').get('api_token'))

    def test_create_duplicate_user(self):
        url = reverse('user-list')
        response = self.client.post(
            path=url, data=self.dup_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('err'), True)
        self.assertEqual(response.json().get(
            'err_code'), errors.ERR_INPUT_VALIDATION)
        self.assertIsNotNone(response.json().get('data'))

    def test_login_existed_user(self):
        response = self.cred_login(
            self.dup_data.get('username'),
            self.dup_data.get('password'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('err'), False)
        self.assertEqual(response.json().get(
            'err_code'), errors.ERR_SUCCESSFUL)
        self.assertIsNotNone(response.json().get(
            'data').get('user').get('access_token'))

    def test_login_nonexistance_user(self):
        response = self.cred_login('undefineduser', 'undefinedpassword')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json().get('err'), True)
        self.assertEqual(response.json().get(
            'err_code'), errors.ERR_DOT_NOT_EXIST)
        self.assertIsNotNone(response.json().get('data'))

    def test_login_wrong_password(self):
        response = self.cred_login(
            self.dup_data.get('username'),
            'wrongpassword')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json().get('err'), True)
        self.assertEqual(response.json().get(
            'err_code'), errors.ERR_AUTHENTICATION_FAILED)
        self.assertIsNotNone(response.json().get('data'))

    def test_logout_anonymous_user(self):
        url = reverse('user-signout')
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('data'), {})

    def test_logout_loggedin_user(self):
        self.auth(self.dup_data.get('username'), self.dup_data.get('password'))
        url = reverse('user-signout')
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('data'), {})

    def test_list_users(self):
        self.auth(self.sup_data.get('username'), self.sup_data.get('password'))
        self._create_sample_users()
        url = reverse('user-list')
        finished = False
        page = 0
        while not finished:
            page += 1
            params = {
                'page': page
            }
            response = self.client.get(path=url, data=params)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json().get('err'), False)
            self.assertEqual(response.json().get(
                'err_code'), errors.ERR_SUCCESSFUL)
            self.assertEqual(
                type(
                    response.json().get('data').get('users')),
                list)
            if response.json().get('data').get('page').get('total_pages') == page:
                finished = True

    def test_list_users_with_api_key(self):
        self.auth(self.sup_data.get('username'),
                  self.sup_data.get('password'), api_key=True)
        self._create_sample_users()
        url = reverse('user-list')
        finished = False
        page = 0
        while not finished:
            page += 1
            params = {
                'page': page
            }
            response = self.client.get(path=url, data=params)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json().get('err'), False)
            self.assertEqual(response.json().get(
                'err_code'), errors.ERR_SUCCESSFUL)
            self.assertEqual(
                type(
                    response.json().get('data').get('users')),
                list)
            if response.json().get('data').get('page').get('total_pages') == page:
                finished = True

    def test_filter_list_users(self):
        self.auth(self.sup_data.get('username'), self.sup_data.get('password'))
        self._create_sample_users()
        url = reverse('user-list')
        finished = False
        page = 0
        while not finished:
            page += 1
            params = {
                'is_active': True,
                'page': page
            }
            response = self.client.get(path=url, data=params)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json().get('err'), False)
            self.assertEqual(response.json().get(
                'err_code'), errors.ERR_SUCCESSFUL)
            self.assertEqual(
                type(
                    response.json().get('data').get('users')),
                list)
            for user in response.json().get('data').get('users'):
                self.assertTrue(user.get('is_active'))
            if response.json().get('data').get('page').get('total_pages') == page:
                finished = True

    def test_filter_by_is_superuser(self):
        self.auth(self.sup_data.get('username'), self.sup_data.get('password'))
        self._create_sample_users()
        url = reverse('user-list')
        params = {'is_superuser': 0}
        response = self.client.get(path=url, data=params)
        self.assertEqual(response.json().get('err'), False)
        self.assertEqual(response.json().get(
            'err_code'), errors.ERR_SUCCESSFUL)
        self.assertEqual(len(response.json().get("data").get("users")), 13)

    def test_change_password_user(self):
        self.auth(self.dup_data.get('username'), self.dup_data.get('password'))
        url = reverse('user-change-password')
        data = {
            'old_password': self.dup_data.get('password'),
            'new_password': 'newpassword'
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('err'), False)
        self.assertEqual(response.json().get(
            'err_code'), errors.ERR_SUCCESSFUL)
        self.assertEqual(response.json().get('data'), {})
        user = User.objects.get(username=self.dup_data.get('username'))
        self.assertTrue(user.check_password)

    def test_change_wrong_password_user(self):
        self.auth(self.dup_data.get('username'), self.dup_data.get('password'))
        url = reverse('user-change-password')
        data = {
            'old_password': 'wrongpassword',
            'new_password': 'newpassword'
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('err'), True)
        self.assertEqual(response.json().get(
            'err_code'), errors.ERR_INPUT_VALIDATION)
        self.assertEqual(response.json().get('data'), {})

    def test_retrieve_user(self):
        self.auth(self.sup_data.get('username'), self.sup_data.get('password'))
        url = reverse('user-detail', args={str(self.dupuser.id)})
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('err'), False)
        self.assertEqual(response.json().get(
            'err_code'), errors.ERR_SUCCESSFUL)
        self.assertEqual(response.json().get('data').get(
            'user').get('id'), str(self.dupuser.id))

    def test_user_profile(self):
        self.auth(self.dup_data.get('username'), self.dup_data.get('password'))
        url = reverse('user-profile')
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('err'), False)
        self.assertEqual(response.json().get(
            'err_code'), errors.ERR_SUCCESSFUL)
        self.assertEqual(response.json().get('data').get(
            'user').get('id'), str(self.dupuser.id))

    def test_user_profile_with_api_token(self):
        url = reverse('user-profile')
        response = self.client.get(path=url, content_type='application/json',
                                   HTTP_PRIVATE_API_KEY=str(self.dupuser.profile.api_token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('err'), False)
        self.assertEqual(response.json().get(
            'err_code'), errors.ERR_SUCCESSFUL)
        self.assertEqual(response.json().get('data').get(
            'user').get('id'), str(self.dupuser.id))

    def test_update_user(self):
        self.auth(self.dup_data.get('username'), self.dup_data.get('password'))
        url = reverse('user-detail', args={str(self.dupuser.id)})
        data = {
            'username': 'newusername',
            'profile': {},
            'email': self.dup_data.get('email'),
            'id': str(self.dupuser.id),
        }
        response = self.client.put(path=url, data=data, format='json')
        response = self.client.put(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('err'), False)
        self.assertEqual(response.json().get(
            'err_code'), errors.ERR_SUCCESSFUL)
        self.assertEqual(response.json().get('data').get(
            'user').get('id'), str(self.dupuser.id))
        self.assertEqual(response.json().get('data').get(
            'user').get('username'), data.get('username'))

    def test_update_user_by_superuser(self):
        self.auth(self.sup_data.get('username'), self.sup_data.get('password'))
        self.dupuser.is_deleted = True
        self.dupuser.is_active = False
        self.dupuser.save()
        url = reverse('user-detail', args={str(self.dupuser.id)})
        data = {
            'is_superuser': True,
        }
        response = self.client.patch(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('err'), False)
        self.assertEqual(response.json().get(
            'err_code'), errors.ERR_SUCCESSFUL)
        self.assertEqual(response.json().get('data').get(
            'user').get('is_superuser'), data.get('is_superuser'))

    def test_soft_delete_user(self):
        self.auth(self.sup_data.get('username'), self.sup_data.get('password'))
        url = reverse('user-detail', args={str(self.dupuser.id)})
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_deactivate_login_failure(self):
        for i in range(4):
            self.cred_login(self.dupuser.username, 'wrongpassword')
        self.assertEqual(User.objects.get(id=self.dupuser.id).is_active, False)
        response = self.cred_login(
            self.dupuser.username,
            self.dup_data.get('password'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json().get('err'), True)
        self.assertEqual(response.json().get(
            'err_code'), errors.ERR_AUTHENTICATION_FAILED)

    def test_user_activate_after_bantime(self):
        for i in range(4):
            self.cred_login(self.dupuser.username, 'wrongpassword')
        user = User.objects.get(id=self.dupuser.id)
        self.assertEqual(user.is_active, False)
        user.banned_at -= timedelta(days=1, hours=2)
        user.save()
        self.auth(self.dup_data.get('username'), self.dup_data.get('password'))
        user = User.objects.get(id=self.dupuser.id)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.failed_login_tries, 0)

    def test_regen_token(self):
        self.auth(self.sup_data.get('username'), self.sup_data.get('password'))
        url = reverse('user-regenerate-token')
        response = self.client.get(path=url)
        self.check_ok_status_code(response)
