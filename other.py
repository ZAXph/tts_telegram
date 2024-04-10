from config import MAX_USER_TTS_SYMBOLS, MAX_TTS_SYMBOLS, TOKEN
import telebot
from repository import DATABASE
from tts import TTS

bot = telebot.TeleBot(token=TOKEN)
table = DATABASE()
tts = TTS()


def is_tts_symbol_limit(message, text):
    text_symbols = len(text)

    # Функция из БД для подсчёта всех потраченных пользователем символов
    all_symbols = int(table.get_data("token", message.from_user.id)[0][0]) + text_symbols

    # Сравниваем all_symbols с количеством доступных пользователю символов
    if all_symbols > MAX_USER_TTS_SYMBOLS:
        msg = f"Превышен общий лимит SpeechKit TTS {MAX_USER_TTS_SYMBOLS}. Использовано: {all_symbols - text_symbols} символов. Доступно: {MAX_USER_TTS_SYMBOLS - all_symbols + text_symbols}"
        bot.send_message(message.chat.id, msg)
        return None

    # Сравниваем количество символов в тексте с максимальным количеством символов в тексте
    if text_symbols >= MAX_TTS_SYMBOLS:
        bot.send_message(message.chat.id,
                         text=f"Превышен лимит SpeechKit TTS на запрос {MAX_TTS_SYMBOLS}, в сообщении {text_symbols} символов")
        return None
    return len(text)


def is_tts_symbol_limit_user(message):
    all_symbols = int(table.get_data("token", message.from_user.id)[0][0])
    if all_symbols == MAX_USER_TTS_SYMBOLS:
        msg = f"Превышен общий лимит SpeechKit TTS {MAX_USER_TTS_SYMBOLS}. Использовано: {all_symbols} символов. Доступно: {MAX_USER_TTS_SYMBOLS - all_symbols}"
        bot.send_message(message.chat.id, msg)
        return None
    return True
