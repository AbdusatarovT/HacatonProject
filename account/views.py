from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from account.serializers import RegisterSerializer, UserLoginSerializer

User = get_user_model()

'''Функция регистрации'''
class RegisterApiView(APIView):
    def post(self, request):
        data = request.data
        serializers = RegisterSerializer(data=data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            massage = f'Успешная регистрация!. Письмо отправленно Вам на почту.'
            return Response(massage, status=201)

'''Функция для активации аккаунта'''
class ActivationView(APIView):
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'msg': 'Ваш аккаунт был активирован'}, status=200)
        except User.DoesNotExist:
            return Response({'msg': 'Неверный код!'}, status=400)


'''функция входа в аккаунт'''
class UserLoginView(APIView):
    def post(self, request):
        data = request.data
        serializers = UserLoginSerializer(data=data)
        if serializers.is_valid(raise_exception=True):
            massage = f'Вы успешно зашли в свой аккаунт!'
            return Response(massage, status=200)





