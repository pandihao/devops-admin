from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from cmdb.models import ServerData
from cmdb.serializers.servers import ServerDataSerializer
from rest_framework.response import Response
import  json
from rest_framework import  status
from rest_framework.decorators import action

class ServerViewSet(ModelViewSet):
    # authentication_classes = []
    # permission_classes = []

    """
    create:
    服务器--新增

    服务器新增, status: 201(成功), return: 新增服务器信息

    destroy:
    服务器--删除

    服务器删除, status: 204(成功), return: None

    multiple_delete:
    服务器--批量删除

    服务器批量删除, status: 204(成功), return: None

    update:
    服务器--修改

    服务器修改, status: 200(成功), return: 修改后的服务器信息

    partial_update:
    服务器--局部修改(服务器授权)

    服务器局部修改, status: 200(成功), return: 修改后的服务器信息

    list:
    服务器--获取列表

    服务器列表信息, status: 200(成功), return: 服务器信息列表
    """
    queryset = ServerData.objects.all()
    serializer_class = ServerDataSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name','ipv4','status','pub_ip')
    ordering_fields = ('name')


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        print('page',page)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            middle_data = serializer.data
            server_data = []
            for instace in middle_data:
                server_dict = {}
                for k, v in instace.items():
                    server_dict[k] = v
                    if k in [ 'tags'] and v is not None:
                        v = json.loads(v.replace("'", "\""))
                    server_dict[k] = v
                server_data.append(server_dict)
            result = server_data

            return self.get_paginated_response(result)

        else:
            serializer = self.get_serializer(queryset, many=True)
            middle_data = serializer.data
            print(middle_data)
            server_data = []
            for instace  in middle_data:
                server_dict = {}
                for k,v in instace.items():
                    if k in ['tags'] and v is not None:
                        v=json.loads(v.replace("'","\""))
                    server_dict[k] = v
                server_data.append(server_dict)
            result = server_data

        return Response(result)

    @action(methods=['delete'], detail=False)
    def multiple_delete(self, request, *args, **kwargs):

        delete_ids = request.data.get('ids')
        print(delete_ids)
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