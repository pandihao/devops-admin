from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from approve.models import CheckApprove
from approve.serializers.check_approve import CheckApproveserializer
from rest_framework.response import Response
from django.db.models.query import QuerySet
import  json
from rest_framework import  status
from rest_framework.decorators import action
from  rest_framework.generics import UpdateAPIView
from django.forms.models import model_to_dict

from django.shortcuts import get_object_or_404 as _get_object_or_404
from django.core.exceptions import ValidationError
from django.http import Http404

def get_object_or_404(queryset, *filter_args, **filter_kwargs):
    """
    Same as Django's standard shortcut, but make sure to also raise 404
    if the filter_kwargs don't match the required types.
    """
    try:
        print(queryset)
        print(filter_kwargs)
        return _get_object_or_404(queryset, *filter_args, **filter_kwargs)
    except (TypeError, ValueError, ValidationError):
        raise Http404



class checkApproveViewSet(ModelViewSet):

    # permission_classes = []
    # authentication_classes = []

    queryset = CheckApprove.objects.all()
    serializer_class = CheckApproveserializer

    def retrieve(self, request, *args, **kwargs):
        # 通过approve_id获取 主键id的字段值，重写pk主键
        self.instance_id = kwargs['pk']
        filter_queryset_dict = self.queryset.filter(approve_id=self.instance_id).values()[0]
        filter_queryset_pk = filter_queryset_dict['id']
        self.kwargs['pk'] = filter_queryset_pk
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        print(serializer.data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        print(request.data)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)