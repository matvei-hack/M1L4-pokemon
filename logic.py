from random import randint
from datetime import datetime, timedelta
import requests

class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = randint(1, 1000)

        data = self.get_data()
        self.name = data['forms'][0]['name'] if data else "pikachu"
        self.img = data['sprites']['other']['official-artwork']['front_default'] if data else None
        self.height = data['height'] if data else None
        self.weight = data['weight'] if data else None
        self.types = [t['type']['name'] for t in data['types']] if data else []
        self.abilities = [a['ability']['name'] for a in data['abilities']] if data else []
        self.base_experience = data['base_experience'] if data else 0

        self.level = 1
        self.exp = 0
        self.hunger = 100
        self.achievements = []

        self.is_rare = self.check_rare()
        if self.is_rare:
            self.achievements.append("Поймал редкого покемона")

        self.hp = randint(50, 100)
        self.power = randint(10, 30)

        # Время последнего кормления (для метода feed с health)
        self.last_feed_time = datetime.now()

        Pokemon.pokemons[pokemon_trainer] = self

    def get_data(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

    def check_rare(self):
        url = f'https://pokeapi.co/api/v2/pokemon-species/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get('is_legendary', False) or data.get('is_mythical', False)
        return False

    def get_name(self):
        return self.name

    def get_img(self):
        return self.img

    def get_height(self):
        return self.height

    def get_weight(self):
        return self.weight

    def get_types(self):
        return self.types

    def get_abilities(self):
        return self.abilities

    def get_base_experience(self):
        return self.base_experience

    def get_level(self):
        return self.level

    def get_hunger(self):
        return self.hunger

    def get_hp(self):
        return self.hp

    def get_power(self):
        return self.power

    def set_name(self, new_name):
        self.name = new_name

    def set_height(self, new_height):
        self.height = new_height

    def set_weight(self, new_weight):
        self.weight = new_weight

    def exp_feed(self):
        gained = randint(5, 20)
        self.exp += gained
        self.hunger = min(100, self.hunger + 30)

        leveled_up = False
        while self.exp >= self.level * 50:
            self.exp -= self.level * 50
            self.level += 1
            leveled_up = True

        if self.level == 5 and "Достиг 5 уровня" not in self.achievements:
            self.achievements.append("Достиг 5 уровня")
        if self.level == 10 and "Достиг 10 уровня" not in self.achievements:
            self.achievements.append("Достиг 10 уровня")

        return gained, leveled_up

    # Исправленный метод кормления — увеличивает здоровье по таймеру
    def feed(self, feed_interval=20, hp_increase=10):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}"
        else:
            next_feed_time = self.last_feed_time + delta_time
            return f"Следующее время кормления покемона: {next_feed_time}"

    def heal(self, amount=20):
        self.hp = min(100, self.hp + amount)
        return self.hp

    def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = randint(1, 5)
            if chance == 1:
                return f"Покемон-волшебник @{enemy.pokemon_trainer} применил щит и уклонился от атаки"

        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}"
        else:
            enemy.hp = 0
            self.exp += 25
            self.achievements.append(f"Победа над @{enemy.pokemon_trainer}")
            return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}. +25 опыта"

    def info(self):
        rare_mark = " РЕДКИЙ" if self.is_rare else ""
        achievements_text = '\n'.join(self.achievements) if self.achievements else "Пока нет"
        return (
            f"Имя твоего покемона: {self.name}{rare_mark}\n"
            f"Уровень: {self.level} (опыт: {self.exp}/{self.level * 50})\n"
            f"Здоровье: {self.hp}\n"
            f"Сила: {self.power}\n"
            f"Сытость: {self.hunger}/100\n"
            f"Рост: {self.height}\n"
            f"Вес: {self.weight}\n"
            f"Типы: {', '.join(self.types)}\n"
            f"Способности: {', '.join(self.abilities)}\n"
            f"Базовый опыт: {self.base_experience}\n"
            f"Достижения:\n{achievements_text}"
        )

    def show_img(self):
        return self.img


class Wizard(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.hp = randint(80, 130)

    def attack(self, enemy):
        return super().attack(enemy)

    # У волшебника здоровье увеличивается больше
    def feed(self, feed_interval=20, hp_increase=20):
        return super().feed(feed_interval, hp_increase)

    def info(self):
        return "У тебя покемон-волшебник\n" + super().info()


class Fighter(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.power = randint(30, 50)

    def attack(self, enemy):
        super_power = randint(5, 15)
        self.power += super_power
        result = super().attack(enemy)
        self.power -= super_power
        return result + f"\nБоец применил супер-атаку силой: {super_power}"

    # У бойца интервал кормления меньше
    def feed(self, feed_interval=10, hp_increase=10):
        return super().feed(feed_interval, hp_increase)

    def info(self):
        return "У тебя покемон-боец\n" + super().info()