import os
import wave

from settings import BASE_DIR
from vendors.tinkoff.python.tinkoff.cloud.stt.v1 import stt_pb2_grpc, stt_pb2
import grpc
from vendors.tinkoff.python.auth import authorization_metadata
from local_settings import ENDPOINT_TINKOFF, API_KEY_TINKOFF, SECRET_KEY_TINKOFF

from pydub import AudioSegment

file_mp3_path = str(os.path.join(BASE_DIR, 'tinkoff_audio_recognition', 'samples', 'file_for_test.mp3'))
file_wav_path = file_mp3_path[:-3] + 'wav'


def wav_maker():
    """
    С помощью библиотеки pydub делаем из mp3 файла wav,
    эта функция понадобится нам ниже, т.к. тинькоф не умеет в распознавание mp3 не в реальном времени
    """

    AudioSegment.from_mp3(file_mp3_path).export(file_wav_path, format="wav")


def build_request():
    """
    Создаем реквест с wav файлом к API тинькоф
    """
    request = stt_pb2.RecognizeRequest()
    with open(file_wav_path, 'rb') as f:
        request.audio.content = f.read()
    request.config.encoding = stt_pb2.AudioEncoding.LINEAR16
    request.config.sample_rate_hertz = 44100

    # Проверка количества каналов в аудио
    with wave.open(file_wav_path, 'rb') as f:
        num_channels = f.getnchannels()
    if num_channels == 1:
        request.config.num_channels = 1
    if num_channels == 2:
        request.config.num_channels = 2
    return request


def recognition_response(response):
    """
    Вспомогательная функция, в которой мы пробегаемся по ответу и достаем именно расшифровку слов
    из аудиофайла
    ВНИМАНИЕ: Если в вашем файле больше 2 дорожек, то он не разберется на слова
    Если расшифровка не совпадает с содержимым файла, проверьте, что приходит в response.result
    """
    ans_str = ''
    for result in response.results:
        for alternative in result.alternatives:
            ans_str += alternative.transcript
        return ans_str


def get_text():
    """
    Для начала вызываем wav_maker для того, чтобы переделать mp3 в понятный для тинькоф wav,
    после уже по файлу wav мы запускаем функции распознавания голоса, ответ выводим через вспомогательную
    функцию recognition_response
    """
    wav_maker()
    stub = stt_pb2_grpc.SpeechToTextStub(grpc.secure_channel(ENDPOINT_TINKOFF, grpc.ssl_channel_credentials()))
    metadata = authorization_metadata(API_KEY_TINKOFF, SECRET_KEY_TINKOFF, 'tinkoff.cloud.stt')

    response = stub.Recognize(build_request(), metadata=metadata)

    return recognition_response(response)
