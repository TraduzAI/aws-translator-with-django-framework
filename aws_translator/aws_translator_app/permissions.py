# aws_translator_app/permissions.py

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Permite que apenas o dono de um objeto possa editá-lo.
    Acesso de leitura é permitido a qualquer pessoa.
    """

    def has_object_permission(self, request, view, obj):
        # Permite leitura para qualquer requisição (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True

        # Permite escrita apenas se o usuário for o dono do objeto
        return obj.owner == request.user
