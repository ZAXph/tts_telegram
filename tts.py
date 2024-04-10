import requests
from config import *


class TTS:
    def __init__(self):
        self.URL = URL
        self.IAM_TOKEN = IAM_TOKEN
        self.VOICE = VOICE
        self.FOLDER_ID = FOLDER_ID

    def text_to_speech(self, text_user):
        headers = {'Authorization': f"Bearer {self.IAM_TOKEN}"}
        data = {'text': text_user,  # текст, который нужно преобразовать в голосовое сообщение
                'lang': 'ru-RU',  # язык текста - русский
                'voice': self.VOICE,  # мужской голос Филиппа
                'folderId': self.FOLDER_ID, }

        response_tts = requests.post(
            self.URL,
            headers=headers,
            data=data
        )
        if response_tts.status_code == 200:
            return True, response_tts.content
        else:
            return False, "При запросе в SpeechKit возникла ошибка"
