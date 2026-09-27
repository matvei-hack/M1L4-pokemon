from random import randint
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
        self.base_experience = data['base_experience'] if data else None

        Pokemon.pokemons[pokemon_trainer] = self

    # Общий запрос к API — чтобы не дёргать его по 5 раз для каждого свойства
    def get_data(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

    # Геттеры
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

    # Сеттеры — изменение свойств
    def set_name(self, new_name):
        self.name = new_name

    def set_height(self, new_height):
        self.height = new_height

    def set_weight(self, new_weight):
        self.weight = new_weight

    # Информация о покемоне
    def info(self):
        return (
            f"Имя твоего покемона: {self.name}\n"
            f"Рост: {self.height}\n"
            f"Вес: {self.weight}\n"
            f"Типы: {', '.join(self.types)}\n"
            f"Способности: {', '.join(self.abilities)}\n"
            f"Базовый опыт: {self.base_experience}"
        )

    def show_img(self):
        return self.img