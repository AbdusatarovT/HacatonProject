from django.contrib.auth import get_user_model
from django.core.mail import send_mail



User = get_user_model()

def send_confirmation_mail(code, email):
    full_link = f'http://localhost:8000/api/account/active/{code}'
    send_mail(
        'Activations code',
        full_link,
        'lgtahir93@gmail.com',
        [email]
    )


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