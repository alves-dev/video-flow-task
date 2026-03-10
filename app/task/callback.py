import logging

import requests

from app.domain.types import VideoDownload, CallbackStatus


def callback(video: VideoDownload, status: CallbackStatus, message: str = None) -> None:
    body = {
        'id': video.id,
        'status': status,
        'message': message
    }

    try:
        response = requests.post(video.url_callback, json=body, headers=None)
        response.raise_for_status()
    except Exception as e:
        logging.error(e)
