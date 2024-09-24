import json
import random
import re
import time
from urllib.parse import unquote
import pathlib
import boto3

TEST_DATA_PATH = pathlib.Path('test_data/group_photos/')


class FunctionError(Exception):
    pass


def get_file_content_from_s3(filename):
    s3 = boto3.client('s3')
    stream = s3.get_object(Bucket='cops-detector-pictures', Key=filename)['Body'].iter_lines()
    content = []
    for i in stream:
        content.append(i.decode('utf-8'))
    json_content = json.loads(''.join(content))
    return json_content


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


def split_file_into_chunks(file_path, no_of_elements_in_chunk):
    with open(file_path, 'r') as f:
        full_list = json.load(f)
        file_path = f.name.split('.')[0]
    chunks = []
    for item in range(0, len(full_list), no_of_elements_in_chunk):
        chunks.append(full_list[item:item + no_of_elements_in_chunk])

    for i, chunk in enumerate(chunks):
        with open(f'{file_path}_{i}.json', 'w+') as f:
            json.dump(chunk, f, ensure_ascii=False)
    return chunks


async def upload_file_to_s3(semaphore, bucket_name, local_file_path):
    async with semaphore:
        remote_file_path = f"pictures/{local_file_path.split('/')[-1]}"
        s3 = boto3.resource('s3')
        s3.Bucket(bucket_name).upload_file(local_file_path, remote_file_path)
        return bucket_name, remote_file_path


def invoke_lamda(function_name: str, payload: dict, invocation_type: str = 'RequestResponse') -> str:
    payload = json.dumps(payload)
    client = boto3.client('lambda')
    response = client.invoke(FunctionName=function_name, InvocationType=invocation_type, Payload=payload)
    return response['ResponseMetadata']

