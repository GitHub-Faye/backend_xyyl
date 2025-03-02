import logging
from django.db import DatabaseError
from django.core.exceptions import ValidationError
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException, NotAuthenticated
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    自定义异常处理函数，增强错误响应
    """
    # 首先调用REST framework默认的异常处理
    response = exception_handler(exc, context)
    
    # 记录错误日志
    logger.error(f"异常发生: {exc}, 上下文: {context['view'].__class__.__name__}")
    
    # 如果默认处理程序没有生成响应，则生成自定义响应
    if response is None:
        if isinstance(exc, DatabaseError):
            response = Response(
                {'detail': '数据库错误，请稍后重试'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        elif isinstance(exc, ValidationError):
            response = Response(
                {'detail': str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif isinstance(exc, ValueError):
            response = Response(
                {'detail': '数据值错误: ' + str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            response = Response(
                {'detail': '服务器内部错误'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            # 记录未处理的异常
            logger.exception("未处理的异常: %s", exc)
    
    # 增强已处理的响应信息
    elif isinstance(exc, NotAuthenticated):
        response.data = {
            'code': 401,
            'message': '用户未认证，请登录',
            'detail': response.data.get('detail', '认证失败')
        }
    elif isinstance(exc, APIException):
        if not response.data.get('code'):
            response.data = {
                'code': response.status_code,
                'message': '请求处理失败',
                'detail': response.data.get('detail', str(exc))
            }
    
    return response 