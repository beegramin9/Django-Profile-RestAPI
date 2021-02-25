# User Authentication
from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """ Allow users to edit their own profile
    Others still can see his profile, but cannot edit it """

    # 이름 똑같이, 업뎃 api가 들어올 때마다 실행됨
    # request, view, permission 확인할 object
    def has_object_permission(self, request, view, obj):
        """ Check if the user is authenticated """
        # Safe HTTP Method: GET,POST 다른것들은 삭제,업뎃하려고 하니까
        # 그냥 보기만 하는건 authentication 없어도 되게끔
        if request.method in permissions.SAFE_METHODS:
            return True

        # 수정하려면 authentication이 필요하게끔
        else:
            # obj(profile)의 id와 request를 보낸 user의 id가 같으면 True
            return obj.id == request.user.id
            # 이게 False로 나오면 개별 /api/profile/1로 들어갔을 때
            # Put, Patch, Delete가 보이지 않는다.


class UpdateOwnStatus(permissions.BasePermission):
    """ Allow users to update thier own status """

    def has_object_permission(self, request, view, obj):
        """ Check the user is trying to update their own status """
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.user_profile.id == request.user.id
