# aws_translator_app/exceptions.py

from ratelimit.exceptions import Ratelimited
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    # Chama o handler padrão primeiro
    response = exception_handler(exc, context)

    # Agora, verifica se a exceção é uma instância de Ratelimited
    if isinstance(exc, Ratelimited):
        return Response(
            {'error': 'Muitas requisições. Por favor, tente novamente mais tarde.'},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )

    return response
