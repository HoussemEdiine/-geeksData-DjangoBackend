import datetime, jwt

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .seriliazer import UserSeriliaze
from rest_framework.exceptions import AuthenticationFailed


# register route

class RegisterUser(APIView):

    def post(self, request):
        seriliazer = UserSeriliaze(data=request.data)
        seriliazer.is_valid(raise_exception=True)
        seriliazer.save()
        return Response(seriliazer.data)

#add uuser
class AddUser(APIView):
    def post(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            return Response({
                'message': 'unauthorized'
            })
        seriliazer = UserSeriliaze(data=request.data)
        seriliazer.is_valid(raise_exception=True)
        seriliazer.save()
        users = User.objects.all()
        seriliazer1 = UserSeriliaze(users,many=True)

        return Response(seriliazer1.data)



# get all users

class GetAllUsers(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            return Response({
                'message': 'unauthorized'
            })
        user = User.objects.all()
        serilizer = UserSeriliaze(user, many=True)
        return Response(serilizer.data)


# delete  user

class DeleteUser(APIView):

    def delete(self, request, pk):
        token = request.COOKIES.get('jwt')
        if not token:
            return Response({
                'message': 'unauthorized'
            })
        user = User.objects.get(id=pk)
        user.delete()
        users = User.objects.all()
        seriliaze = UserSeriliaze(users, many=True)
        return Response(seriliaze.data)


# update user


class UpdateUser(APIView):

    def get_object(self, pk):

        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response('USER do not exisit')

    def put(self, request, pk):
        token = request.COOKIES.get('jwt')
        if not token:
            return Response({
                'message': 'unauthorized'
            })
        userobj = self.get_object(pk)
        serilaizer = UserSeriliaze(userobj, data=request.data)
        if serilaizer.is_valid():
            serilaizer.save()

        return Response(serilaizer.data)


# login
class LoginUser(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        # check if user exist
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('user not found')

        if not user.check_password(password):
            raise AuthenticationFailed('password incorrect')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secretword', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            token
        }

        return response
