import requests


def add_file(but, activity: dict, file_mp3_path: str) -> int:
    """
    Функция получает файл по ссылке и пытается записать его
    @but - Токен авторизации
    @activity: dict - Активити, которое содержит в себе id файла
    @file_mp3_path: str - Путь к файлу
    """
    file_id = activity['FILES'][0]['id']

    result = but.call_list_method('disk.file.get', {'id': file_id})
    response = requests.get(result['DOWNLOAD_URL'])
    if response.status_code == 200:
        with open(file_mp3_path, 'wb') as f:
            f.write(response.content)
        return response.status_code
    else:
        return response.status_code