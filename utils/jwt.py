import jwt
from datetime import datetime, timedelta
from django.conf import settings


class JwtHelper(object):
    @staticmethod
    def encode(payload: dict) -> str:
        data = {
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow()+ timedelta(days=1)}
        for key, value in payload.items():
            data[key] = value
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token

    @staticmethod
    def decode(token: str) -> dict:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
