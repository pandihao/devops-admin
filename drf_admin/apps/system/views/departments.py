
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_admin.utils.views import TreeAPIView
from rest_framework.viewsets import ModelViewSet
from system.models import Departments
from system.serializers.departments import DepartmentsSerializer ,DepartmentsTreeSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import  status
from django.db.models.query import QuerySet

class DepartmentsViewSet(ModelViewSet,TreeAPIView):
    """
    create:
    部门--新增

    部门新增, status: 201(成功), return: 新增部门信息

    destroy:
    部门--删除

    部门删除, status: 204(成功), return: None

    multiple_delete:
    部门--批量删除

    部门批量删除, status: 204(成功), return: None

    update:
    部门--修改

    部门修改, status: 200(成功), return: 修改增部门信息

    partial_update:
    部门--局部修改

    部门局部修改, status: 200(成功), return: 修改增部门信息

    list:
    部门--获取列表

    部门列表信息, status: 200(成功), return: 部门信息列表
    """

    queryset = Departments.objects.all()
    serializer_class = DepartmentsSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id', 'name')

    def get_serializer_class(self):
        if self.action == 'list':
            return DepartmentsTreeSerializer
        else:
            return DepartmentsSerializer


    @action(methods=['delete'], detail=False)
    def multiple_delete(self, request, *args, **kwargs):
        delete_ids = request.data.get('ids')
        if not delete_ids:
            return Response(data={'detail': '参数错误,ids为必传参数'}, status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(delete_ids, list):
            return Response(data={'detail': 'ids格式错误,必须为List'}, status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        del_queryset = queryset.filter(id__in=delete_ids)
        if len(delete_ids) != del_queryset.count():
            return Response(data={'detail': '删除数据不存在'}, status=status.HTTP_400_BAD_REQUEST)
        del_queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)