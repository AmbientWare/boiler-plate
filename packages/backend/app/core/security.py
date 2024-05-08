import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from cryptography.fernet import Fernet
import json

from app.core import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "1ccpyf10wM"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

cipher_suite = Fernet(config.get_app_settings().ENCRYPTION_KEY)


def hash_text(text: str) -> str:
    return pwd_context.hash(text)


def verify_hash(input: str, hash: str) -> bool:
    return pwd_context.verify(input, hash)


def create_api_key(
    *, data: dict, expires_delta: Optional[timedelta] = None, never_expire: bool = False
):
    to_encode = data.copy()
    if not never_expire:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=15)
        to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_api_key(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return "Signature has expired"
    except jwt.InvalidTokenError:
        return "Invalid token"
    except Exception as e:
        return e


def encrypt_json_data(data):
    # Serialize JSON data to bytes
    json_bytes = json.dumps(data, sort_keys=True).encode()

    # Encrypt the JSON bytes
    encrypted_data = cipher_suite.encrypt(json_bytes)

    return encrypted_data


def decrypt_json_data(encrypted_data):
    # Decrypt the encrypted data
    decrypted_data = cipher_suite.decrypt(encrypted_data)

    # Deserialize decrypted bytes to JSON
    json_data = json.loads(decrypted_data.decode())

    return json_data
