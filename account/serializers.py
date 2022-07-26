from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from account.utils import send_confirmation_mail

User = get_user_model()

'''Сериалазер для регистрации'''
class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(min_length=8, max_length=10, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2')

        if password != password2:
            raise serializers.ValidationError('Пароль не совподает!')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        code = user.activation_code
        send_confirmation_mail(code, user.email)
        return User

'''Сериалайзер для входа в аккаунт'''
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Такой пользователь не зарегистрирован!')
        return email

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Вы указали неверный email или пароль!')
            attrs['user'] = user
            return attrs


