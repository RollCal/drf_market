from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """
    객체의 소유주만 수정 및 삭제가 가능
    """

    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모두에게 허용
        if request.method in permissions.SAFE_METHODS:
            return True

        # 작성, 수정, 삭제 권한은 소유주에게만 허용
        return obj.user == request.user
