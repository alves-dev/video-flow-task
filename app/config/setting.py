import uuid

import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Security
    AUTH_ENABLED: bool = True
    SECURITY_API_KEY: str = str(uuid.uuid4())

    OUTPUT_FOLDER: str = '/tmp'

    WHISPER_MODEL: str = 'base'

    # SOS
    SOS_URL: str = 'https://sos.alves-dev.com'
    SOS_API_KEY: str
    SOS_BUCKET: str = 'video-flow-transcriptions'

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


dotenv.load_dotenv()
setting = Settings()
