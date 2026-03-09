import subprocess
import logging
from fastapi import APIRouter, BackgroundTasks
from fastapi.params import Depends

from app.api.core.security import check_api_key
from app.api.requests import VideoDownload

router = APIRouter(prefix='/api/v1')


def baixar_video(url: str):
    folder_output = "output"

    comando = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "--output", f"{folder_output}/%(title)s.%(ext)s",
        url
    ]

    try:
        subprocess.run(comando, check=True)
        logging.info("✅ Download concluído com sucesso!")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Erro ao baixar: {e}")
    except FileNotFoundError:
        logging.error("❌ yt-dlp não encontrado. Instale com: pip install yt-dlp")


@router.post("/download", dependencies=[Depends(check_api_key)])
def video_download(video: VideoDownload, background_tasks: BackgroundTasks) -> bool:
    try:
        background_tasks.add_task(baixar_video, video.url)
        return True
    except Exception as e:
        logging.error(e)
        return False
