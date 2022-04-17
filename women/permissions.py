""" Создать свой класс Permission """
from rest_framework import permissions



class IsAdminOrReadOnly(permissions.BasePermission):
    """ чтоб читать могли все. а удалять только админ """
    def has_permission(self, request, view): # для всех записей
        if request.method in permissions.SAFE_METHODS: # это такие только для чтения
            return True # True - значит права доступа предоставлены

        return bool(request.user and request.user.is_staff) # юзер залогинен И юзер - админ



class IsOwnerOrReadOnly(permissions.BasePermission):
    """ Менять запись может только создатель, читать - все"""

    def has_object_permission(self, request, view, obj): # для конкретной записи
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user # первый user - название поля в модели




