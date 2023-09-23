from .models import User


def _get_sample_user_data(username=None, password=None, email=None, superuser=None, active=None):
    data = {
        'email': 'test@example.com' if email is None else email,
        'username': 'test' if username is None else username,
        'password': 'test' if password is None else password
    }
    if active is not None:
        data["is_active"] = active
    if superuser is not None:
        data["is_superuser"] = superuser
    return data


def get_sample_user_data(username=None, password=None, email=None, superuser=None, active=None):
    user = _get_sample_user_data(username=username, password=password,
                                 email=email, superuser=superuser, active=active)
    return user


def get_sample_user(username=None, password=None, email=None, superuser=None, active=None):
    user = _get_sample_user_data(username=username, password=password,
                                 email=email, superuser=superuser, active=active)
    return User.objects.create(**user)


def get_sample_user_profile(username=None, password=None, email=None, superuser=None, active=None):
    user_data = _get_sample_user_data(username=username, password=password,
                                      email=email, superuser=superuser, active=active)
    user = User.objects.create(**user_data)
    return user.profile


def get_sample_user_with_password():
    data = {
        'username': 'testuser',
        'password': 'testpassword',
        'email': 'test@example.com',
    }
    return User.objects.create(**data), data.get('password')


def get_sample_superuser_with_password():
    data = {
        'username': 'testuser',
        'password': 'testpassword',
        'email': 'test@example.com',
    }
    return User.objects.create_superuser(**data), data.get('password')
