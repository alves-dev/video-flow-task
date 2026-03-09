from fastapi import HTTPException
from fastapi.params import Header

from app.config.setting import setting


def check_api_key(x_api_key: str = Header(None)):
    if not setting.AUTH_ENABLED:
        return

    if x_api_key != setting.SECURITY_API_KEY:
        raise HTTPException(status_code=401, detail="API Key inválida")