from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from account.utils import send_confirmation_mail
from django.core.mail import send_mail

User = get_user_model()


'''Сериалазер для регистрации'''
class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(min_length=8, write_only=True, required=True)

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
        # print(email)
        return email

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        # print(password)
        if email and password:
            user = authenticate(username=email, password=password)
            # print(user)
            if not user:
                raise serializers.ValidationError('Вы указали неверный email или пароль!')
            attrs['user'] = user
            return attrs

'''Сериалайзер для изменения пароля'''
class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    new_password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'new_password2']

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError('Указаные пароли не совпадают')
        return attrs

    def validate_old_password(self, p):
        user = self.context.get('request').user
        if not user.check_password(p):
            raise serializers.ValidationError('Неверный пароль!')
        return p

    def update(self):
        user = self.context.get('request').user
        password = self.validated_data.get('password')
        user.set_password(password)
        user.save()


'''Сериалайзер для Востановления пароля через почту'''
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не зарегистрирован')
        return email

    def send_code(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.code_generation()
        user.save()
        send_mail(
            'Восстановление пароля',
            f'Ваш код подтверждения: {user.activation_code}',
            'lgtahir93@gmail.com',
            [email]
        )


class ForgotPasswordCompleteSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(min_length=8, max_length=8, required=True)
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)

    def validate_email(self, email):
        print(email)
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не зарегистрирован')
        return email

    def validate_code(self, code):
        print(code)
        if not User.objects.filter(activation_code=code).exists():
            print(code)
            raise serializers.ValidationError('Пользователь не зарегистрирован')
        return code

    def validate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.get('password_confirm')
        if pass1 != pass2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def set_new_pass(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.activation_code = ''
        user.save()