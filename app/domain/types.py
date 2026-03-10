from dataclasses import dataclass
from typing import Callable
from enum import Enum

from pydantic import BaseModel


class CallbackStatus(Enum):
    TRANSCRIBED = 'TRANSCRIBED'
    DOWNLOADED = 'DOWNLOADED'


class VideoDownload(BaseModel):
    id: str
    url: str
    url_callback: str


@dataclass
class Task:
    name: str
    func: Callable
    args: tuple
