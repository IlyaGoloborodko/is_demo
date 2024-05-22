def attach_transcription(but, speech_to_text: str, call_id: str):
    """
    Функция прикрепляет расшифровку к звонку
    @but - токен
    @speech_to_text: str - текст расшифровки
    @call_id: str - id звонка
    """
    messages = [
        {
            'SIDE': 'User',
            'START_TIME': 1,
            'STOP_TIME': 3,
            'MESSAGE': speech_to_text
        }]
    but.call_api_method('telephony.call.attachTranscription', {
        'CALL_ID': call_id,
        'MESSAGES': messages
    })