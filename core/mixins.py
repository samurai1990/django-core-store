from django.core.cache import caches
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from .decorators import serializer_validation

EXPIARY = 60*60*3  # 3 hours


class UpdateModelMixin:
    def perform_update(self, serializer):
        return serializer.save()


class CreateMixin(mixins.CreateModelMixin):
    @serializer_validation
    def create(self, request, *args, **kwargs):
        reqser = self.get_serializer(data=request.data)
        reqser.is_valid(raise_exception=True)
        model = self.perform_create(reqser)
        resser = self.get_serializer_response()(model)
        return Response(
            data={model._meta.verbose_name.lower(): resser.data},
            status=HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()


class UpdateMixin(UpdateModelMixin):
    @serializer_validation
    def update(self, request, pk, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        model = self.perform_update(serializer)
        resser = self.get_serializer_response()(model)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(data={model._meta.verbose_name.lower(): resser.data})


class PartialUpdateMixin(UpdateModelMixin):
    def partial_update(self, request, pk, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        model = self.perform_update(serializer)
        resser = self.get_serializer_response()(model)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(data={model._meta.verbose_name.lower(): resser.data})


class IdempotentUpdateMixin(UpdateModelMixin):
    @serializer_validation
    def update(self, request, pk, *args, **kwargs):
        key = hash(f'{request.user.id},{request.data},{pk}')
        is_idempotent = caches['idempotent'].get(key)
        if is_idempotent:
            return Response(
                data={self.queryset.model.__name__.lower(): request.data})
        else:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            model = self.perform_update(serializer)
            resser = self.get_serializer_response()(model)
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            caches['idempotent'].set(key, 1, EXPIARY)
            return Response(
                data={model._meta.verbose_name.lower(): resser.data})

    def perform_update(self, serializer):
        return serializer.save()


class RetrieveMixin(mixins.RetrieveModelMixin):
    def retrieve(self, request, *args, **kwargs):
        kwargs = request.query_params
        instance = self.get_object()
        resser = self.get_serializer_response()(instance, *args, **kwargs)
        return Response(
            data={instance._meta.verbose_name.lower(): resser.data})


class DestroyMixin(mixins.DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={}, status=HTTP_204_NO_CONTENT)


class ListMixin(mixins.ListModelMixin):
    def list(self, request, *args, **kwargs):
        if request.query_params.get('page', None) is not None:
            return super().list(request, args, kwargs)
        else:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {self.queryset.model._meta.verbose_name_plural: serializer.data})
