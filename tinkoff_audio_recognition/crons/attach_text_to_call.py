import os
import requests

from settings import BASE_DIR
from tinkoff_audio_recognition.funcs.get_token import get_bitrix_token

def attach_text_cron():
    but = get_bitrix_token()

    res = but.call_list_method('crm.activity.list', {'filter':
                                                    {
                                                        'PROVIDER_ID': 'VOXIMPLANT_CALL',
                                                        '>CREATED': '2024-05-22T00:00:00+03:00',
                                                    }
    })

    file_mp3_path = str(os.path.join(BASE_DIR, 'tinkoff_audio_recognition', 'samples', 'file_for_test.mp3'))

    filtered_activities = [activity for activity in res if 'FILES' in activity and activity['FILES']]

    for activity in filtered_activities:

        file_id = activity['FILES'][0]['id']

        result = but.call_list_method('disk.file.get', {'id': file_id})
        response = requests.get(result['DOWNLOAD_URL'])
        if response.status_code == 200:
            with open(file_mp3_path, 'wb') as f:
                f.write(response.content)


def add_new_call():
    but = get_bitrix_token()

    res_call = but.call_api_method("telephony.externalcall.register", {
        "USER_PHONE_INNER": 2576,
        "USER_ID": 2567,
        "PHONE_NUMBER": 78013457684,
        "TYPE": 1,
        "CRM_CREATE": 1,
    })

    but.call_api_method('telephony.externalcall.finish', {
        "CALL_ID": res_call['result']['CALL_ID'],
        "USER_ID": 2567,
        "DURATION": 61,
        "RECORD_URL": "https://cdn-ru.bitrix24.ru/b26806988/voximplant/312/31229a711c9f3236a9b03f11da068833/d7a00e4e70032f466a505d63661e88ee.mp3",
    })