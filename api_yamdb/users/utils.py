import hashlib

from django.core.mail import send_mail

from api_yamdb.settings import SECRET_KEY


def generate_activation_code(username: str) -> str:
    code_bytes = (SECRET_KEY + username).encode('utf-8')
    hash_code = hashlib.sha256(code_bytes)
    return hash_code.hexdigest()


def send_confirmation_code(username, recipient):
    confirmation_code = generate_activation_code(username)
    send_mail(
        subject='Register',
        message=f'Registration success, your {confirmation_code=}',
        from_email='yamdb@yamdb.ru',
        recipient_list=[recipient],
        fail_silently=True)
