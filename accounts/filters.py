from rest_framework.filters import BaseFilterBackend
from distutils.util import strtobool


class ActiveUserFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        try:
            is_active = request.query_params.get('is_active', None)
            if is_active is not None:
                return queryset.filter(is_active__in=[strtobool(is_active.capitalize())])
            else:
                return queryset
        except Exception:
            return queryset


class DeletedUserFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        try:
            is_deleted = request.query_params.get('is_deleted', None)
            if is_deleted is not None:
                return queryset.filter(is_deleted__in=[strtobool(is_deleted.capitalize())])
            else:
                return queryset
        except Exception:
            return queryset


class SuperUserFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        try:
            is_superuser = request.query_params.get('is_superuser', None)
            if is_superuser is not None:
                return queryset.filter(is_superuser__in=[strtobool(is_superuser.capitalize())])
            else:
                return queryset
        except Exception:
            return queryset
