import ipaddress
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_ipv4_network(value):
    try:
        ipaddress.IPv4Network(value)
    except ValueError:
        raise ValidationError(_('Enter a valid IPv4 network.'), code='invalid', params={'value': value})


def validate_ipv6_network(value):
    try:
        ipaddress.IPv6Network(value)
    except ValueError:
        raise ValidationError(_('Enter a valid IPv6 network.'), code='invalid', params={'value': value})


def validate_ipv46_network(value):
    try:
        validate_ipv4_network(value)
    except ValidationError:
        try:
            validate_ipv6_network(value)
        except ValidationError:
            raise ValidationError(_('Enter a valid IPv4 or IPv6 network.'), code='invalid', params={'value': value})


def validate_port(value):
    if value in range(0, 65537):
        pass
    else:
        raise ValidationError(_('Enter a valid port.'), code='invalid', params={'value': value})