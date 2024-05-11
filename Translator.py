from langdetect import detect
from playsound import playsound
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import pyttsx3
import pycountry

# Initialize text-to-speech engineH
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Function to detect language
def detect_language(text):
    try:
        lang_code = detect(text)
        language = pycountry.languages.get(alpha_2=lang_code)
        return language.name
    except Exception as e:
        print("Error detecting language:", e)
        return None


# Function to take voice input
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print(f"User said: {query}")
        return query
    except Exception as e:
        print("Error recognizing speech:", e)
        return None


# Function to get destination language
def destination_language():
    print("Enter the language you want to translate to (e.g., Hindi, English, Spanish):")
    destination_lang = input("Language: ").strip().lower()
    return destination_lang


# Function to translate text
def translate_text(text, dest_lang):
    translator = Translator()
    translation = translator.translate(text, dest=dest_lang)
    return translation.text


# Function to speak translated text
def speak_translated_text(text, dest_lang):
    try:
        speak(f"Translating to {dest_lang}")
        tts = gTTS(text=text, lang=dest_lang, slow=False)
        tts.save("translation.mp3")
        playsound("translation.mp3")
        os.remove("translation.mp3")
    except Exception as e:
        print("Error speaking translated text:", e)


# Main function
def main():
    print("Welcome to the Translator!")
    speak("Welcome to the Translator!")

    while True:
        try:
            # Get input from user
            speak("Please say the sentence you want to translate.")
            text = take_command()
            if text is None:
                continue

            # Detect language
            from_lang = detect_language(text)
            if from_lang:
                print("Detected language:", from_lang)
                speak(f"I detected that the sentence is in {from_lang}.")
            else:
                print("Error detecting language.")
                speak("Sorry, I couldn't detect the language.")
                continue

            # Get destination language
            dest_lang = destination_language()

            # Translate text
            translated_text = translate_text(text, dest_lang)
            print("Translated text:", translated_text)

            # Speak translated text
            speak_translated_text(translated_text, dest_lang)

            # Ask if user wants to continue
            speak("Do you want to translate another sentence? Yes or No.")
            response = take_command()
            if response and "no" in response.lower():
                speak("Goodbye!")
                break
        except Exception as e:
            print("An error occurred:", e)
            speak("Sorry, an error occurred. Please try again.")


if __name__ == "__main__":
    main()
