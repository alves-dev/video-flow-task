from pydantic import BaseModel


class VideoDownload(BaseModel):
    url: str
