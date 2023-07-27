import hashlib

from api_yamdb.settings import SECRET_KEY


def generate_activation_code(username: str) -> str:
    code_bytes = (SECRET_KEY + username).encode('utf-8')
    hash_code = hashlib.sha256(code_bytes)
    return hash_code.hexdigest()
