import logging

import requests

from app.domain.types import VideoDownload, CallbackStatus


def callback(video: VideoDownload, status: CallbackStatus, data: dict = None) -> None:
    body = {
        'id': video.id,
        'status': status,
        'data': data
    }

    try:
        response = requests.post(video.url_callback, json=body, headers=None)
        response.raise_for_status()
    except Exception as e:
        logging.error(e)
