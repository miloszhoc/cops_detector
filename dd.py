from transformers import BertTokenizer, BertModel
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained("bert-base-uncased")
text = "Replace me by any text you'd like."
encoded_input = tokenizer(text, return_tensors='pt')
output = model(**encoded_input)
print(output)



# from gpt4all import GPT4All
#
# model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")  # downloads / loads a 4.66GB LLM
# with model.chat_session():
#     print(model.generate("""
#     UWAGA BIAŁYSTOK, NOWY RADIOWÓZ !\n\nSkoda Octavia III Drogówki z Białegostoku (Woj. Podlaskie)\nSilnik: 1,8 Turbo / 180 KM\nWyposażenie: 2 kamery polcam\nNadzorowany teren: Miasto Białystok i Powiat białostocki. Droga S8, Drogi Krajowe numer 8, 19, 65 oraz Drogi Wojewódzkie numer: 676, 678.\nBIA 28075\n\n#Policja #Radiowóz #Białystok #Videorejestrator #Skoda #Octavia3 #Drogówka #Podlaskie #BIA28075 #nieoznakowaneradiowozy Pokaż mniej
#
#     z powyższych informacji wyciągnij polską nazwę województwa i miasta, marka i model samochodu, aktualny polski numer rejestracyjny pojazdu skadający sie z cyfr i liter, jeśli są, to poprzednie numery rejestracyjne i polskie numery dróg po których pojazd się porusza. wyniki zapisz w formacie json o strukturze:
#     {voivodeship : nazwa województwa (string),
#     city: miasto (string),
#     car_info: marka i model samochodu (string),
#     current_licence_plate_number: aktualny polski numer rejestracyjny pojazdu skadający sie z cyfr i liter (string)
#     old_license_plates: poprzednie numery rejestracyjne (list),
#     road_numbers: polskie numery dróg po których pojazd się porusza (list),
#     }
#     jeśli brakuje danych, to pozostaw puste pole.
#     """, max_tokens=1024))
