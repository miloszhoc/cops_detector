from dataclasses import dataclass
from enum import Enum


@dataclass
class WebsiteData:
    base_url: str


class Website(WebsiteData, Enum):
    NIEOZNAKOWANY = 'https://nieoznakowany.pl'
    FACEBOOK = 'https://facebook.com'
