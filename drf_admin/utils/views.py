from rest_framework import  serializers
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView


class TreeSerializer(serializers.ModelSerializer):
    """
    TreeAPIView使用的基类序列化器
    """
    id = serializers.IntegerField()
    label = serializers.CharField(max_length=20, source='name')
    pid = serializers.PrimaryKeyRelatedField(read_only=True)

class TreeAPIView(ListAPIView):
    """
    定义Element Tree树结构
    """
    # pagination_class=None

    def list(self, request, *args, **kwargs):
        '''
          self.get_queryset() ：  方法是调用GenericAPIView 中的get_queryset() 方法，返回值: class 中的queryset 的查询集的全部返回结果， queryset.all() 方法
          self.filter_queryset(queryset): 基于filter_backends中的条件过滤类方法 [SearchFilter,OrderingFilter]
          self.paginate_queryset(queryset) : 筛选返回指定page页的数据
          SearchFilter ，OrderingFilter 中都有filter_queryset 方法
          SearchFilter.filter_queryset() 通过search_fields 字段返回新的查询集内容

        '''

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        '''
         GenericAPIView 中的get_serializer_class 方法，返回值为 self.serializer_class
         get_serializer 调用get_serializer_class() 方法， 返回值 self.serializer_class(queryset) ,序列化查询集中的数据，得到序列化对象
        '''
        serializer = self.get_serializer(queryset, many=True)
        '''
        page 是必须传递参数 ，重写list方法。 因重写了前端展示方式，把原序列化数据格式重新封装
        '''
        tree_dict = {}
        tree_data = []
        try:
            for item in serializer.data:
                tree_dict[item['id']] = item
            for i in tree_dict:
                if tree_dict[i]['pid']:
                    pid = tree_dict[i]['pid']
                    parent = tree_dict[pid]
                    parent.setdefault('children', []).append(tree_dict[i])
                else:
                    tree_data.append(tree_dict[i])
            results = tree_data
        except KeyError:
            results = serializer.data

        print('results {}'.format(results))
        if page is not None:
            '''
            默认配置了全局分页，所以一定会有page类的调用。如果前端页面不需要分页，可以设置pagination_class=None。 由于分页返回Response的对象数据格式特殊，需要修改前端axios请求返回值
            '''
            print('page result {}'.format(self.get_paginated_response(results)))
            return self.get_paginated_response(results)
        return Response(results)


class ChoiceAPIView(APIView):
    """
    model choice字段API, 需指定choice属性或覆盖get_choice方法
    """
    choice = None

    def get(self, request):
        methods = [{'value': value[0], 'label': value[1]} for value in self.get_choice()]
        return Response(data={'results': methods})

    def get_choice(self):
        assert self.choice is not None, (
                "'%s' 应该包含一个`choice`属性,或覆盖`get_choice()`方法."
                % self.__class__.__name__
        )
        assert isinstance(self.choice, tuple) and len(self.choice) > 0, 'choice数据错误, 应为二维元组'
        for values in self.choice:
            assert isinstance(values, tuple) and len(values) == 2, 'choice数据错误, 应为二维元组'
        return self.choice
