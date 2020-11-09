from rest_framework import generics
from .models import MyUsers
from rest_framework.response import Response
from .serializer import UserSerializer, CreateUserSerializer, EditUserSerializer, ChangePassworSerializer, EditAvatar
from rest_framework import permissions, status, parsers
from .permissions import user_permission


class Profile(generics.ListCreateAPIView):
    parser_classes = (parsers.MultiPartParser, parsers.JSONParser, parsers.FileUploadParser, )

    def get(self, request, *args, **kwargs):
        try:
            serializer = UserSerializer(request.user)
            res = {'data': serializer.data}
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            respone = {"message": "Error"}
            return Response(respone, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            user = request.user
            serializer = EditUserSerializer(user, request.data)
            # import pdb; pdb.set_trace()
            if serializer.is_valid():
                serializer.save()
                user = serializer.data.copy()
                return Response(user, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            respone = {"message": "Error"}
            return Response(respone, status=status.HTTP_400_BAD_REQUEST)


class Avatar(generics.ListCreateAPIView):
    parser_classes = (parsers.MultiPartParser, parsers.JSONParser, parsers.FileUploadParser, )
    
    def post(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        try:
            user = request.user
            serializer = EditAvatar(user, request.data)
            if serializer.is_valid():
                serializer.save()
                avatar = serializer.data.copy()
                return Response(avatar, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise e
            respose = {"message": "Đã có lỗi sảy ra, bạn vui lòng thử lại"}
            return Response(respose, status=status.HTTP_400_BAD_REQUEST)


class CreateUser(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = CreateUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                user = serializer.data.copy()
                user.pop('password')
                user_permission(user['id'])
                return Response({"user": user}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise e
            respone = {"message": "Error"}
            return Response(respone, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(generics.ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            old_password = request.data['old_password']
            if user.check_password(old_password):
                user.set_password(request.data['password'])
                user.save()
                respone = {"message": "Thay đổi mật khẩu thành công"}
                return Response(respone, status=status.HTTP_200_OK)
            else:
                respone = {"message": "Mật khẩu cũ không đúng, vui lòng nhập lại"}
                return Response(respone, status=status.HTTP_400_BAD_REQUEST)
        except:
            respone = {"message": "Đã có lỗi sảy ra. Bạn vui lòng thử lại sau"}
            return Response(respone, status=status.HTTP_400_BAD_REQUEST)


class Logout(generics.ListCreateAPIView):
    def get(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
