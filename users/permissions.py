# -*- coding:utf-8 -*-
from rest_framework import permissions


class IsModerPermission(permissions.BasePermission):
    message = 'Доступ открыт только модераторам'

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moders').exists()

class IsOwnerPermission(permissions.BasePermission):
    message = 'Доступ открыт только владельцев'
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

