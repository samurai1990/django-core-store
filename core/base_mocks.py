from django.core.files import File as DjangoFile


def get_django_file(path):
    return DjangoFile(open(path, mode='rb'))
