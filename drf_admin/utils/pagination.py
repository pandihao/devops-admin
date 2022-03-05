
from rest_framework.pagination import PageNumberPagination

class GlobalPagination(PageNumberPagination):
    page_query_param = 'page'  # 前一个字符串值，指示用于分页控件的查询参数的名称。
    page_size = 10  #  分页功能在没有使用size参数请求的的情况下，每页默认返回的数据条数。现在前端调用时候会使用page_size_query_param这个参数，会标明size大小，数实际值会与前端参数一致。
    page_size_query_param = 'size'  # 如果设置，这是一个字符串值，指示允许客户端根据每个请求设置页面大小的查询参数的名称。默认值为 None，表示客户端可能无法控制请求的页面大小。
    max_page_size = 1000  # 如果设置，这是一个数字值，指示允许的最大请求页面大小。此属性仅在设置了 page_size_query_param 时有效。
