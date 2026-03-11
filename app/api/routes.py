import logging

from fastapi import APIRouter
from fastapi.params import Depends

from app.api.core.security import check_api_key
from app.domain.types import Task, VideoDownload
from app.task import video as video_task
from app.task import audio as audio_task
from app.task.task_queue import task_queue

router = APIRouter(prefix='/api/v1')


@router.post("/download", dependencies=[Depends(check_api_key)])
def video_download(video: VideoDownload) -> bool:
    try:
        task_video_download = Task(
            name=f"download-{video.id}",
            func=video_task.download,
            args=(video,)
        )

        task_transcribe = Task(
            name=f"transcribe-{video.id}",
            func=audio_task.transcribe,
            args=(video,)
        )

        task_queue.add_task(task_video_download)
        task_queue.add_task(task_transcribe)
        return True
    except Exception as e:
        logging.error(e)
        return False
