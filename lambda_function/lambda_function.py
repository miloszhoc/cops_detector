import google.generativeai as genai
import os


def lambda_handler(event, context):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash',
                                  generation_config={"response_mime_type": "application/json"})

    prompt = f"""
            {event['description']}

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

    response = model.generate_content(prompt)
    print(response.text)

    return {'statusCode': 200,
            'body': response.text}
