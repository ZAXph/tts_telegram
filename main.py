from other import is_tts_symbol_limit, is_tts_symbol_limit_user, bot, table, tts


@bot.message_handler(commands=["start"])
def start_bot(message):
    bot.send_message(chat_id=message.chat.id,
                     text="Привет! Доступна команда:\n/tts - После написания команды, отправь боту текст и он его озвучит.")


@bot.message_handler(commands=["tts"])
def expectation_text(message):
    result = table.get_data("user_id", message.from_user.id)
    if (message.from_user.id,) not in result:
        table.add_data(message.from_user.id)
        print("Добавление в базу данных")
    elif is_tts_symbol_limit_user(message) is None:
        print("У пользователя закончились токены")
        return
    bot.send_message(chat_id=message.chat.id, text="Отправь свой текст")
    bot.register_next_step_handler(message, processing_text)


def processing_text(message):
    if message.content_type != "text":
        bot.send_message(chat_id=message.chat.id, text="Вы отправили не текст! Отправь свой текст.")
        bot.register_next_step_handler(message, processing_text)
    else:
        len_text = is_tts_symbol_limit(message, message.text)
        if len_text != len(message.text):
            msg = bot.send_message(chat_id=message.chat.id, text="Поменяйте текст:")
            bot.register_next_step_handler(msg, processing_text)
        else:
            success, response = tts.text_to_speech(message.text)
            if success:
                tokens = table.get_data("token", message.from_user.id)[0][0]
                table.update_data(message.from_user.id, "token", int(tokens) + len_text)
                with open(f'voice/{message.from_user.id}.ogg', 'wb') as audio_file:
                    audio_file.write(response)
                voice = open(f'voice/{message.from_user.id}.ogg', 'rb')
                bot.send_voice(chat_id=message.chat.id, voice=voice)
                voice.close()
                bot.send_message(chat_id=message.chat.id, text="Новый запрос: /tts")
            else:
                bot.send_message(chat_id=message.chat.id, text="Что-то пошло не так!")
                

if __name__ == "__main__":
    table.create_table()
    bot.polling()
