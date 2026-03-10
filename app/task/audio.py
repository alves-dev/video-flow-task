import logging
import os

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

        callback(video, CallbackStatus.TRANSCRIBED, 'Transcrito com sucesso.')

    except Exception as e:
        logging.error(e)
