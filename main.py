import telebot
from config import token
from logic import Pokemon

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['go'])
def go(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        pokemon = Pokemon(message.from_user.username)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(commands=['mypokemon'])
def mypokemon(message):
    username = message.from_user.username
    if username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[username]
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "У тебя ещё нет покемона, создай его командой /go")


@bot.message_handler(commands=['feed'])
def feed(message):
    username = message.from_user.username
    if username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[username]
        gained, leveled_up = pokemon.feed()
        text = f"Ты покормил {pokemon.get_name()}! +{gained} опыта."
        if leveled_up:
            text += f"\n🎉 Покемон вырос до уровня {pokemon.get_level()}!"
        bot.reply_to(message, text)
    else:
        bot.reply_to(message, "Сначала создай покемона командой /go")



@bot.message_handler(commands=['rename'])
def rename(message):
    username = message.from_user.username
    if username in Pokemon.pokemons.keys():
        new_name = message.text.replace('/rename', '').strip()
        if new_name:
            Pokemon.pokemons[username].set_name(new_name)
            bot.reply_to(message, f"Теперь твоего покемона зовут {new_name}")
        else:
            bot.reply_to(message, "Напиши новое имя после команды, например: /rename Пикачу")
    else:
        bot.reply_to(message, "Сначала создай покемона командой /go")

bot.infinity_polling(none_stop=True)