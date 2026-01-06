from rest_framework import permissions

class IsModer(permissions.BasePermission):


    def has_permission(self, request, view):
        return request.user.groups.filter(name='moders').exists()

class IsModerAndUser(permissions.BasePermission):


    def has_permission(self, request, view):
        return request.user.groups.filter(name='moders').exists() or request.user.groups.filter(name='user').exists()

