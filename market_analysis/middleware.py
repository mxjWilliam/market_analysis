import logging

logger = logging.getLogger(__name__)

class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            logger.error(f"An unhandled exception occurred: {str(e)}", exc_info=True)
            # 可以返回自定义的错误响应
            from django.http import HttpResponseServerError
            return HttpResponseServerError('Internal Server Error')