import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import pygame
import requests

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something in Kannada...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="kn-IN")
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def translate_to_english(text):
    translator = Translator()
    translation = translator.translate(text, dest='en')
    return translation.text
statename='Karnataka'
def get_crop_price_english(crop_name, state='Karnataka'):
    api_key = '579b464db66ec23bdd000001877ac7662958412b7a49de4e2e55a6d0'
    api_url = 'https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070'

    params = {
        'api-key': api_key,
        'format': 'json',
        'filters[commodity]': crop_name,
        'filters[state]':"Karnataka"
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        records = data.get('records', [])

        if not records:
            print(f"No data found for {crop_name} in  {state}")
        else:
            for record in records:
                
                print(f"Market: {record.get('market')}, Arrival Date: {record.get('arrival_date')}, Modal Price: {record.get('modal_price')}")
                speak(f" ಬರವಿ ದಿನಾಂಕ: {record.get('arrival_date')},  ಬೆಲೆ: {record.get('modal_price')}")
                break
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

def speak(text):
    kannada_text = gTTS(text=text, lang='kn', slow=False)
    kannada_text.save("output.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()
    

    # Block until the audio finishes playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()

    # Remove the audio file after playing
    os.remove("output.mp3")

def main():
    while True:
        input_text = recognize_speech()
        if input_text:
            print(f"You said (Kannada): {input_text}")

            if input_text.lower() == 'exit':
                break

            english_text = translate_to_english(input_text)
            print(f"In English: {english_text}")
            speak(input_text)
            get_crop_price_english(english_text)
            

if __name__ == "__main__":
    main()
