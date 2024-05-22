import openai

from django.conf import settings
from settings import BASE_DIR
import os

openai.api_key = settings.OPEN_AI_API_KEY


def open_ai_get_text():
    audio_file = open(str(os.path.join(BASE_DIR, 'tinkoff_audio_recognition',
                                       'samples', 'file_for_test.mp3')), 'rb')
    transcript = openai.Audio.transcribe('whisper-1', audio_file)
    audio_file.close()
    return transcript.text
