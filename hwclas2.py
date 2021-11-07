import json
import random
from abc import ABC, abstractmethod


#Задание 1: задачи с лекции
class AnimeMon(ABC):
    @property
    @abstractmethod
    def exp(self):
        pass

    @classmethod
    @abstractmethod
    def inc_exp(cls, exp_size):
        pass


class Pokemon(AnimeMon):
    def __init__(self, name: str, poketype: str):
        self.name = name
        self.poketype = poketype
        self.exp = 0

    def to_str(self):
        return f'{self.name}/{self.poketype}'

    def exp(self):
        return self.exp

    def inc_exp(self, exp_size):
        self.exp += exp_size


class Digimon(AnimeMon):
    def __init__(self, name: str):
        self.name = name
        self.exp = 0

    def exp(self):
        return self.exp

    def inc_exp(self, exp_size):
        self.exp += exp_size*8


def train(pokemon: Pokemon):
    step_size, level_size = 10, 100
    sparring_qty = (level_size - pokemon.exp % level_size) // step_size
    for i in range(sparring_qty):
        win = random.choice([True, False])
        if win:
            pokemon.inc_exp(step_size)


class JsonToObj(dict):
    """
    Наследуемся от dict и рекурсивно "переводим" ключи словаря в атрибуты
    """
    def __init__(self, data):
        pass
        super(JsonToObj, self).__init__()
        for key, value in data.items():
            if isinstance(value, dict):
                value = JsonToObj(value)
            setattr(self, key, value)
            self.update({key: value})


class ColorizeMixin:
    """
    Меняем цвет вывода миксином
    """
    def __repr__(self):
        return f'\033[1;{self.repr_color_code};40m {self.title} | {self.price} ₽'


class Advert(ColorizeMixin, JsonToObj):
    """
    Наследуемся от миксина и JsonToObj, проводим проверки на цену и инициализируемся от JsonToObj
    """
    def __init__(self, data):
        if 'price' in data:
            if data['price'] < 0:
                raise ValueError("must be >= 0")
        else:
            self.price = 0
        super(Advert, self).__init__(data)

    def __repr__(self):
        self.repr_color_code = 33
        return ColorizeMixin.__repr__(self)


if __name__ == '__main__':
    agumon = Digimon(name='Agumon')
    train(agumon)
    print(agumon.exp)
    bulbasaur = Pokemon(name='Bulbasaur', poketype='grass')
    train(bulbasaur)
    print(bulbasaur.exp)
    sample_item_json = """{
    "title": "iPhone X",
    "price": 100,
    "location": {
    "address": "город Самара, улица Мориса Тореза, 50",
    "metro": {
    "metro_line": "красная",
    "metro_stations": ["Комсомольская", "Спортивная"]
    }
    }
    }"""
    sample_item = json.loads(sample_item_json)
    class_item = Advert(sample_item)
    print(class_item.location.address)
    print(class_item.location.metro)
    print(class_item.location.metro.metro_stations)
    print(class_item)