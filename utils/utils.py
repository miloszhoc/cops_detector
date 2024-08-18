import asyncio
import json
import re
import time
from urllib.parse import unquote

import boto3


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


def add_timestamp(input_str, ext='jpg'):
    return f'{input_str}_{int(time.time())}.{ext}'


async def upload_file_to_s3(semaphore, bucket_name, local_file_path):
    async with semaphore:
        remote_file_path = f"pictures/{local_file_path.split('/')[-1]}"
        s3 = boto3.resource('s3')
        s3.Bucket(bucket_name).upload_file(local_file_path, remote_file_path)
        return bucket_name, remote_file_path
