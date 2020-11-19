from rest_framework import status


NOT_PERMISSION = {
    "message": ["Bạn không có quyền truy cập chức năng này"]
}


def check_permission(request, perm):
    if request.user.has_perm(perm):
        user = request.user
        return True, user, status.HTTP_200_OK
    else:
        return False, NOT_PERMISSION, status.HTTP_400_BAD_REQUEST