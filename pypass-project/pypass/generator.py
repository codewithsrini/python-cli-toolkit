import secrets
import string

def generate_password(length: int = 16, use_symbols: bool = False) -> str:
  alphabet = string.ascii_letters + string.digits

  if use_symbols:
    alphabet += string.punctuation

  return "".join(secrets.choice(alphabet) for _ in range(length))
