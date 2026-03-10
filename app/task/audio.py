import logging
import os

import requests
from faster_whisper import WhisperModel

from app.config.setting import setting
from app.domain.types import VideoDownload, CallbackStatus
from app.task.callback import callback


def transcribe(video: VideoDownload):
    try:
        logging.info(f"🔄 Carregando modelo '{setting.WHISPER_MODEL}'")
        model = WhisperModel(setting.WHISPER_MODEL, device="cpu", compute_type="int8")

        mp3_file = f'{setting.OUTPUT_FOLDER}/videos/{video.id}.mp3'

        logging.info(f"🎙️ Transcrevendo '{mp3_file}'")
        segments, info = model.transcribe(mp3_file, language="pt")

        logging.info(f"Idioma detectado: {info.language} (confiança: {info.language_probability:.0%})\n")

        os.makedirs(f'{setting.OUTPUT_FOLDER}/transcribe', exist_ok=True)
        transcribe_txt = f'{setting.OUTPUT_FOLDER}/transcribe/{video.id}.txt'

        with open(transcribe_txt, "w", encoding="utf-8") as f:
            for segment in segments:
                linha = segment.text.strip()
                f.write(linha + "\n")

        logging.info(f"\n✅ Transcrição salva em: {transcribe_txt}")

        response = _upload_transcription(transcribe_txt)

        callback(video, CallbackStatus.TRANSCRIBED, {'transcribe_file_url': response['data']['url']})

    except Exception as e:
        logging.error(e)


def _upload_transcription(file_path, metadata_json=None):
    headers = {
        "X-API-Key": setting.SOS_API_KEY
    }
    data = {
        "bucket": setting.SOS_BUCKET,
        "isPublic": True
    }

    if metadata_json:
        data["metadata"] = metadata_json

    try:
        files = {
            "file": open(file_path, "rb")
        }

        response = requests.post(
            f'{setting.SOS_URL}/api/files/upload',
            headers=headers,
            files=files,
            data=data
        )

        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Erro ao enviar transcrição: {e}")
        return None
