from dataclasses import dataclass
from enum import Enum, unique


@dataclass
class VoivodeshipData:
    readable_name: str
    url_param_name: str


@unique
class Voivodeship(VoivodeshipData, Enum):
    DOLNOSLASKIE = 'dolnośląskie', 'dolnoslaskie'
    KUJAWSKO_POMORSKIE = 'kujawsko - pomorskie', 'kujawsko_pomorskie'
    LUBELSKIE = 'lubelskie', 'lubelskie'
    LUBUSKIE = 'lubuskie', 'lubuskie'
    LODZKIE = 'łódzkie', 'lodzkie'
    MALOPOLSKIE = 'małopolskie', 'malopolskie'
    MAZOWIECKIE = 'mazowieckie', 'mazowieckie'
    OPOLSKIE = 'opolskie', 'opolskie'
    PODKARPACKIE = 'podkarpackie', 'podkarpackie'
    PODLASKIE = 'podlaskie', 'podlaskie'
    POMORSKIE = 'pomorskie', 'pomorskie'
    SLASKIE = 'śląskie', 'slaskie'
    SWIETOKRZYSKIE = 'świętokrzyskie', 'swietokrzyskie'
    WARMINSKO_MAZURSKIE = 'warmińsko - mazurskie', 'warminsko_mazurskie'
    WIELKOPOLSKIE = 'wielkopolskie', 'wielkopolskie'
    ZACHODNIOPOMORSKIE = 'zachodniopomorskie', 'zachodniopomorskie'
