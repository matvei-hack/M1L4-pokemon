from random import randint
import telebot
from config import token
from logic import Pokemon, Wizard, Fighter

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['go'])
def go(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        chance = randint(1, 20)
        if chance <= 14:
            pokemon = Pokemon(message.from_user.username)
        elif chance <= 17:
            pokemon = Wizard(message.from_user.username)
        else:
            pokemon = Fighter(message.from_user.username)

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

@bot.message_handler(commands=['info'])
def info(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pok = Pokemon.pokemons[message.from_user.username]
        bot.send_message(message.chat.id, pok.info())
    else:
        bot.reply_to(message, "Сначала создай покемона командой /go")

# Начисление опыта и уровня
@bot.message_handler(commands=['train'])
def train(message):
    username = message.from_user.username
    if username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[username]
        gained, leveled_up = pokemon.exp_feed()
        text = f"Ты потренировал {pokemon.get_name()}. +{gained} опыта."
        if leveled_up:
            text += f" Уровень вырос до {pokemon.get_level()}."
        bot.reply_to(message, text)
    else:
        bot.reply_to(message, "Сначала создай покемона командой /go")

# Кормление для здоровья (с таймером last_feed_time)
@bot.message_handler(commands=['feed'])
def feed(message):
    username = message.from_user.username
    if username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[username]
        result = pokemon.feed()
        bot.reply_to(message, result)
    else:
        bot.reply_to(message, "Сначала создай покемона командой /go")

@bot.message_handler(commands=['heal'])
def heal(message):
    username = message.from_user.username
    if username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[username]
        new_hp = pokemon.heal()
        bot.reply_to(message, f"Твой покемон восстановил здоровье. Текущее HP: {new_hp}")
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

@bot.message_handler(commands=['attack'])
def attack_pok(message):
    if message.reply_to_message:
        attacker_name = message.from_user.username
        target_name = message.reply_to_message.from_user.username

        if target_name in Pokemon.pokemons.keys() and attacker_name in Pokemon.pokemons.keys():
            enemy = Pokemon.pokemons[target_name]
            pok = Pokemon.pokemons[attacker_name]
            res = pok.attack(enemy)
            bot.send_message(message.chat.id, res)
        else:
            bot.send_message(message.chat.id, "Сражаться можно только с покемонами")
    else:
        bot.send_message(message.chat.id, "Чтобы атаковать, нужно ответить на сообщение того, кого хочешь атаковать")

@bot.message_handler(commands=['battle'])
def battle(message):
    username = message.from_user.username
    if username not in Pokemon.pokemons.keys():
        bot.reply_to(message, "Сначала создай покемона командой /go")
        return

    pokemon = Pokemon.pokemons[username]

    chance = randint(1, 20)
    if chance <= 14:
        enemy = Pokemon("дикий_покемон")
    elif chance <= 17:
        enemy = Wizard("дикий_покемон")
    else:
        enemy = Fighter("дикий_покемон")

    log = [f"{pokemon.get_name()} против дикого {enemy.get_name()}"]
    log.append(f"HP: {pokemon.get_hp()} vs {enemy.get_hp()}")

    round_num = 1
    while pokemon.hp > 0 and enemy.hp > 0 and round_num <= 10:
        result = pokemon.attack(enemy)
        log.append(f"Раунд {round_num}: {result}")
        if enemy.hp <= 0:
            break
        result = enemy.attack(pokemon)
        log.append(f"Раунд {round_num} (ответ): {result}")
        round_num += 1

    if pokemon.hp <= 0 and enemy.hp <= 0:
        log.append("Ничья")
    elif pokemon.hp <= 0:
        log.append(f"Твой покемон проиграл дикому {enemy.get_name()}")
    elif enemy.hp <= 0:
        log.append(f"Ты победил дикого {enemy.get_name()}")
    else:
        log.append("Бой закончился вничью по лимиту раундов")

    bot.send_message(message.chat.id, '\n'.join(log))

bot.infinity_polling(none_stop=True)