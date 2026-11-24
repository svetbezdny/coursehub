import base64
import hashlib
import hmac
import secrets
import time
from typing import Any

import jwt
from jwt.exceptions import InvalidTokenError

HASH_ITERATIONS = 600_000


def hash_password(password: str) -> str:
    salt = secrets.token_urlsafe(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        HASH_ITERATIONS,
    )
    encoded_digest = base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
    return f"pbkdf2_sha256${HASH_ITERATIONS}${salt}${encoded_digest}"


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        algorithm, iterations_text, salt, expected_digest = hashed_password.split(
            "$", 3
        )
        iterations = int(iterations_text)
        if iterations <= 0:
            return False
    except ValueError:
        return False
    if algorithm != "pbkdf2_sha256":
        return False
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        iterations,
    )
    actual_digest = base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
    return hmac.compare_digest(actual_digest, expected_digest)


def create_access_token(
    *,
    subject: str,
    secret_key: str,
    expires_in_seconds: int,
) -> str:
    issued_at = int(time.time())
    payload = {
        "sub": subject,
        "iat": issued_at,
        "exp": issued_at + expires_in_seconds,
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")


def decode_access_token(token: str, *, secret_key: str) -> dict[str, Any] | None:
    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=["HS256"],
            options={"require": ["exp", "iat", "sub"]},
        )

        if type(payload["exp"]) is not int or type(payload["iat"]) is not int:
            return None
        return payload
    except InvalidTokenError:
        return None
