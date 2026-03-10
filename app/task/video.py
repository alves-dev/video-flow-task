import logging
import subprocess

from app.config.setting import setting
from app.domain.types import VideoDownload, CallbackStatus
from app.task.callback import callback


def download(video: VideoDownload):
    comando = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "--output", f"{setting.OUTPUT_FOLDER}/videos/{video.id}.%(ext)s",
        video.url
    ]

    try:
        subprocess.run(comando, check=True)
        logging.info("✅ Download concluído com sucesso!")

        callback(video, CallbackStatus.DOWNLOADED, 'Baixado com sucesso')

    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Erro ao baixar: {e}")
    except FileNotFoundError:
        logging.error("❌ yt-dlp não encontrado. Instale com: pip install yt-dlp")
