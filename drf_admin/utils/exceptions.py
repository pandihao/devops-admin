from rest_framework.views import exception_handler as drf_excepion_handler
from django.db import DatabaseError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ErrorDetail




def errors_handler(exc):
    """
    自定义, 错误消息格式处理
    :param exc:
    :return: data: 错误消息
    """
    try:
        if isinstance(exc.detail, list):
            msg = ''.join([str(x) for x in exc.detail])
        elif isinstance(exc.detail, dict):
            def search_error(detail: dict, message: str):
                for k, v in detail.items():
                    if k == 'non_field_errors':
                        if isinstance(v, list) and isinstance(v[0], ErrorDetail):
                            message += ''.join([str(x) for x in v])
                        else:
                            message += str(v)
                    else:
                        if isinstance(v, list) and isinstance(v[0], ErrorDetail):
                            message += str(k)
                            message += ''.join([str(x) for x in v])
                        elif isinstance(v, list) and isinstance(v[0], dict):
                            for value_dict in v:
                                message = search_error(value_dict, message)
                return message

            msg = ''
            msg = search_error(exc.detail, msg)
        else:
            msg = exc.detail
        if not msg:
            msg = exc.detail
    except Exception:
        msg = exc.detail
    data = {'detail': msg}
    return data



def exception_handler(exc, context):
    response = drf_excepion_handler(exc, context)
    # print('exception_handler function')
    print('exc detail',exc)
    print(response)
    # print('%s - %s - %s' % (context['view'], context['request'].method, exc))
    if response:
        response.data = errors_handler(exc)


    if response is None:
        if isinstance(exc, DatabaseError):
            # 数据库异常
            # view = context['view']
            # # 数据库记录异常
            # print('[%s]: %s' % (view, exc))
            response = Response(data={"type": "数据异常","detail": str(exc)}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
        else:
            response = Response(data={"type": "未知异常", "detail": str(exc)}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response