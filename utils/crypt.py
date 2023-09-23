from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
from django.conf import settings
from core.exceptions import InternalError
from logging import getLogger

logger = getLogger('django')


def encrypt(data):
    try:
        passphrase = urlsafe_b64encode(bytes(settings.PASSWORDPHRASE, 'utf-8'))
        fernet = Fernet(passphrase)
        cypertext=fernet.encrypt(data.encode('utf-8'))
        return cypertext.decode("utf-8")
    except ValueError as err:
        logger.error("during exception encrypt with error: {0}".format(err))
        raise InternalError("Ecryption Failed")


def decrypt(ciphertext):
    try:
        passphrase = urlsafe_b64encode(bytes(settings.PASSWORDPHRASE, 'utf-8'))
        fernet = Fernet(passphrase)
        return fernet.decrypt(ciphertext).decode('utf-8')
    except ValueError as err:
        logger.error("during exception decrypt with error: {0}".format(err))
        raise InternalError("Decryption Failed")
