# from transformers import BertTokenizer, BertModel
#
# tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
# model = BertModel.from_pretrained("bert-base-uncased")
# text = "Replace me by any text you'd like."
# encoded_input = tokenizer(text, return_tensors='pt')
# output = model(**encoded_input)
# print(output)
#
import time

from gpt4all import GPT4All

start_time = int(time.time())
print(start_time)
# model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf", device='cuda')  # downloads / loads a 4.66GB LLM
model = GPT4All("Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf", device='cuda')
with model.chat_session():
    resp = model.generate("""
    UWAGA BIAŁYSTOK, NOWY RADIOWÓZ !\n\nSkoda Octavia III Drogówki z Białegostoku (Woj. Podlaskie)\nSilnik: 1,8 Turbo / 180 KM\nWyposażenie: 2 kamery polcam\nNadzorowany teren: Miasto Białystok i Powiat białostocki. Droga S8, Drogi Krajowe numer 8, 19, 65 oraz Drogi Wojewódzkie numer: 676, 678.\nBIA 28075\n\n#Policja #Radiowóz #Białystok #Videorejestrator #Skoda #Octavia3 #Drogówka #Podlaskie #BIA28075 #nieoznakowaneradiowozy Pokaż mniej

    From the above information presented in Polish, extract the Polish name of the province and city, make and model of car, current Polish vehicle registration number consisting of numbers and letters. If there are, previous registration numbers and Polish numbers of roads on which the vehicle moves. save the results in json format with the structure:
    {voivodeship : province name (string),
    city: city (string),
    car_info: car make and model (string),
    current_licence_plate_number: current Polish vehicle registration number consisting of numbers and letters (string)
    old_license_plates: previous registration numbers (list),
    road_numbers: Polish numbers of roads on which the vehicle moves (list),
    }
    if data is missing, leave blank. Return only the json.
    """, max_tokens=1024)
    print(resp)
end_time = int(time.time())

print(f'execution time {end_time - start_time}sek.')
