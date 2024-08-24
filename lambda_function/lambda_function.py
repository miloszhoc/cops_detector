import json
import time

import boto3
import google.generativeai as genai
import os
import tempfile


def get_file_content_from_s3(filename):
    s3 = boto3.client('s3')
    stream = s3.get_object(Bucket='cops-detector-pictures', Key=filename)['Body'].iter_lines()
    content = []
    for i in stream:
        content.append(i.decode('utf-8'))
    json_content = json.loads(''.join(content))
    return json_content


def upload_to_s3(file_name, bucket, object_name=None):
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"File '{file_name}' uploaded to '{bucket}/{object_name}' successfully.")
    except Exception as e:
        print(f"Failed to upload {file_name} to S3: {str(e)}")


def lambda_handler(event, context):
    source_json_content = get_file_content_from_s3(event['source_filename'])

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash',
                                  generation_config={"response_mime_type": "application/json"})

    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as temp_file:
        for item in source_json_content[:2]:
            try:
                item['llm_extracted']
            except KeyError:
                prompt = f"""
                        {item['description']}
            
                        From the above information presented in Polish, extract the Polish name of the province and city, make and model of car, current Polish vehicle registration number consisting of numbers and letters. If there are, previous registration numbers and Polish numbers of roads on which the vehicle moves. save the results in json format with the structure:
                        {{voivodeship : province name (string),
                        city: city (string),
                        car_info: car make and model (string),
                        current_licence_plate_number: current Polish vehicle registration number consisting of numbers and letters (string)
                        old_license_plates: previous registration numbers (list),
                        road_numbers: Polish numbers of roads on which the vehicle moves (list),
                        }}
                        if data is missing, leave blank. Return only the json structure and nothing else.
                        """
            else:
                print('NOTHING TO DO')
            response = model.generate_content(prompt)
            print(response.text)
            item['llm_extracted'] = json.loads(response.text)
        time.sleep(1)

        destination_json_content = get_file_content_from_s3(event['destination_filename'])
        destination_json_content.extend(source_json_content)
        json.dump(destination_json_content, temp_file, indent=3, ensure_ascii=False)

        temp_file_name = temp_file.name

    upload_to_s3(temp_file_name, 'cops-detector-pictures', event['destination_filename'])

    return {'statusCode': 200,
            'body': response.text}
