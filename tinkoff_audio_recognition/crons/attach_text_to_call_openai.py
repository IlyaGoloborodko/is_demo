import os

from settings import BASE_DIR
from tinkoff_audio_recognition.funcs.get_token import get_bitrix_token

from tinkoff_audio_recognition.models import ProcessingTime
from tinkoff_audio_recognition.funcs.open_ai_stt import open_ai_get_text
from tinkoff_audio_recognition.funcs.attach_transcription import attach_transcription
from tinkoff_audio_recognition.funcs.add_file import add_file


def attach_text_cron_openai():
    """
    Крон-функция для получения всех звонков с записями,их последующей расшифровки и прикрепления расшифровки к звонку
    """
    but = get_bitrix_token()

    # Проверка наличия объектов в модели
    if not ProcessingTime.objects.exists():
        # Если объектов нет, создаем новый объект с указанным значением last_time
        default_time = '2024-05-22T00:00:00+03:00'
        processing_time = ProcessingTime.objects.create(last_time=default_time)
    else:
        # Если объект существует, получаем его
        processing_time = ProcessingTime.objects.first()

    res = but.call_list_method('crm.activity.list', {'filter': {
        'PROVIDER_ID': 'VOXIMPLANT_CALL',
        '>CREATED': processing_time}
    })

    if res:
        file_mp3_path = str(os.path.join(BASE_DIR, 'tinkoff_audio_recognition', 'samples', 'file_for_test.mp3'))
        filtered_activities = [activity for activity in res if 'FILES' in activity and activity['FILES']]

        for activity in filtered_activities:
            # Получаем файл и сохраняем его в файловой системе
            status = add_file(but, activity, file_mp3_path)
            if status == 200:
                # Преобразуем файл в текст
                speech_to_text = open_ai_get_text()
                if len(speech_to_text) > 0:
                    call_id = activity['ORIGIN_ID'][3:]
                    # Прикрепляем расшифровку к звонку
                    attach_transcription(but, speech_to_text, call_id)

            last_time = activity['START_TIME']

        processing_time.last_time = last_time
        processing_time.save()


def add_new_call():
    but = get_bitrix_token()

    res_call = but.call_api_method("telephony.externalcall.register", {
        "USER_PHONE_INNER": 2576,
        "USER_ID": 2567,
        "PHONE_NUMBER": 78013457681,
        "TYPE": 1,
        "CRM_CREATE": 1,
    })

    but.call_api_method('telephony.externalcall.finish', {
        "CALL_ID": res_call['result']['CALL_ID'],
        "USER_ID": 2567,
        "DURATION": 61,
        "RECORD_URL": "https://drive.google.com/uc?export=download&id=1uINhWxSOE1yxVtqEq9PNsgFoRJXsg3cD",
    })
