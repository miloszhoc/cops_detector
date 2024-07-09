import re
from urllib.parse import unquote


def extract_data_from_urls(urls):
    car_data = {}
    for url in urls:
        data = re.search(
            r'registry=([\w\s\*]*)&province=([\w\s]*)&brand=([\w\s\/]*)&model=([\w\s\(\)\-\']*)&color=([\w\s\-]*)&county=([\w\s]*)',
            unquote(url))
        register_no = data.group(1)
        province = data.group(2)
        brand = data.group(3)
        model = data.group(4)
        color = data.group(5)
        country = data.group(6)
        car_data[register_no] = {'register_no': register_no,
                                 'voivodeship': province,
                                 'brand': brand,
                                 'model': model,
                                 'color': color,
                                 'city': country}
    return car_data
