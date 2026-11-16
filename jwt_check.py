import os
from urllib.parse import urlparse, parse_qs
import jwt as pyjwt
from dotenv import load_dotenv

load_dotenv()
JWT_SECRET = os.environ["JWT_SECRET"]


def extract_token(handler):
    auth = handler.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth[7:]
    q = parse_qs(urlparse(handler.path).query)
    return (q.get("token") or [None])[0]


def verify_token(token):
    if not token:
        return None
    try:
        payload = pyjwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload.get("sub")
    except pyjwt.PyJWTError:
        return None


def require_auth(handler):
    """Возвращает email, если токен валиден. Иначе отправляет 401 и None."""
    email = verify_token(extract_token(handler))
    if not email:
        handler.send_response(401)
        handler.send_header("Content-Type", "application/json")
        handler.send_header("Access-Control-Allow-Origin", "*")
        handler.end_headers()
        handler.wfile.write(b'{"error":"unauthorized"}')
        return None
    return email