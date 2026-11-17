import base64
import hashlib
import hmac
import secrets


PASSWORD_ITERATIONS = 600_000


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    derived = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PASSWORD_ITERATIONS
    )
    return "pbkdf2_sha256${}${}${}".format(
        PASSWORD_ITERATIONS,
        base64.urlsafe_b64encode(salt).decode("ascii").rstrip("="),
        base64.urlsafe_b64encode(derived).decode("ascii").rstrip("="),
    )


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, iteration_text, salt_text, digest_text = stored_hash.split("$")
        if algorithm != "pbkdf2_sha256":
            return False
        iterations = int(iteration_text)
        if not 100_000 <= iterations <= 2_000_000:
            return False
        salt = base64.urlsafe_b64decode(salt_text + "=" * (-len(salt_text) % 4))
        expected = base64.urlsafe_b64decode(
            digest_text + "=" * (-len(digest_text) % 4)
        )
        actual = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, iterations
        )
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def hash_session_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def new_session_secret() -> str:
    return secrets.token_urlsafe(32)
