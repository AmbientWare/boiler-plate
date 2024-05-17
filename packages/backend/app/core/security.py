import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from cryptography.fernet import Fernet
import json
import base64
from typing import Union

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

    # Encode the encrypted data into a Base64 string to safely store/transport
    encrypted_base64 = base64.urlsafe_b64encode(encrypted_data).decode("utf-8")

    return encrypted_base64


def decrypt_json_data(encrypted_data) -> Union[dict, None]:
    # Decode the Base64 encoded encrypted data to bytes
    try:
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode("utf-8"))
    except Exception as e:
        return None

    # Decrypt the encrypted bytes
    try:
        decrypted_data = cipher_suite.decrypt(encrypted_bytes)
    except Exception as e:
        return None

    # Deserialize decrypted bytes to JSON
    try:
        json_data = json.loads(decrypted_data.decode())
    except json.JSONDecodeError as e:
        return None

    return json_data
