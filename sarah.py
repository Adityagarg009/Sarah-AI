import speech_recognition as sr
import pyttsx3
import webbrowser as wb
import datetime
import wikipedia
import pyjokes
import pywhatkit
from googletrans import Translator

def initialize_engine():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Female voice command
    return engine
def introduce(engine):
    print ("Greetings! I'm Sarah, your trusty AI assistant. I'm here to assist you with any tasks, questions, or conversations you might have. Whether you need help with research, want to brainstorm ideas, or simply crave a friendly chat, I'm at your service. Think of me as your digital sidekick, always ready to lend a hand and make your day a little bit easier. So, what can I assist you with today?")
    engine.say("Greetings! I'm Sarah, your trusty AI assistant. I'm here to assist you with any tasks, questions, or conversations you might have. Whether you need help with research, want to brainstorm ideas, or simply crave a friendly chat, I'm at your service. Think of me as your digital sidekick, always ready to lend a hand and make your day a little bit easier. So, what can I assist you with today?")
    engine.runAndWait()
def play(text, engine):
    song = text.replace('play', '')
    engine.say("As per your request, playing the song " + song)
    engine.runAndWait()
    pywhatkit.playonyt(song)
def get_wikipedia_summary(person_name, engine):
    try:
        page = wikipedia.page(person_name)
        summary = wikipedia.summary(person_name, sentences=2)
        print("Summary:", summary)
        engine.say("According to my knowledge, " + summary)
        engine.say("For further knowledge, visit this link given below")
        engine.runAndWait()
        wikipedia_link = "https://en.wikipedia.org/wiki/" + page.title.replace(" ", "_")
        print("Wikipedia Link:", wikipedia_link)
        engine.say(wikipedia_link)
        engine.runAndWait()
    except wikipedia.exceptions.PageError:
        print("Sorry, I couldn't find a Wikipedia page for that person.")
        engine.say("Sorry, I couldn't find a Wikipedia page for that person.")
        engine.runAndWait()
    except wikipedia.exceptions.DisambiguationError as e:
        print("There are multiple results for this query. Please be more specific.")
        engine.say("There are multiple results for this query. Please be more specific.")
        engine.runAndWait()

def get_voice_input(prompt, recognizer, engine):
    print(prompt)
    engine.say(prompt)
    engine.runAndWait()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=3)  # Adjust duration if necessary
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print("Recognized Text:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand your voice.")
        engine.say("Sorry, I could not understand your voice.")
        engine.runAndWait()
        return None
    except sr.RequestError as e:
        print("Error fetching results. Check your internet connection.", e)
        engine.say("Error fetching results. Check your internet connection.")
        engine.runAndWait()
        return None

def get_date_time():
    current_datetime = datetime.datetime.now()
    formatted_date_time = current_datetime.strftime("%A, %B %d, %Y %I:%M %p")
    return formatted_date_time          

def opening(text, engine):
    def extract_command(input_text):
        words = input_text.split()
        for i, word in enumerate(words):
            if word.lower() == 'open' and i + 1 < len(words):
                return words[i + 1]
    command = extract_command(text)
    if command:
        engine.say(f"As per your wish, opening {command}")
        engine.runAndWait()
        if command.lower() == "youtube":
            opening_url = "https://www.youtube.com/"
        elif command.lower() == "spotify":
            opening_url = "https://open.spotify.com/"
        elif command.lower() == "youtubemusic":
            opening_url = "https://music.youtube.com/"
        else:
            opening_url = f"https://www.google.com/search?q={command}"
        wb.open(opening_url, new=2)

def translate(text, destination_language, engine):
    translator = Translator()
    translation = translator.translate(text, dest=destination_language)
    translated_text = translation.text
    print("Translated Text:", translated_text)
    voices = engine.getProperty('voices')
    for voice in voices:
        try:
            if destination_language.lower() in voice.languages[0].lower():
                engine.setProperty('voice', voice.id)
                break
        except IndexError:
            continue
    engine.say("Translated Text:")
    engine.say(translated_text)
    engine.runAndWait()

engine = initialize_engine()
recognizer = sr.Recognizer()

while True:
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Hello! How may I help you?")
        engine.say("Hello! How may I help you?")
        engine.runAndWait()
        print("listening")
        audio = recognizer.listen(source, timeout=6)
        print('Ok, Searching....')
        engine.say("Ok, Searching")
        engine.runAndWait()
    try:
        text = recognizer.recognize_google(audio, show_all=False)
        print("Recognized Text:", text)
        if "open" in text.lower():
            opening(text, engine)
        elif "translate" in text.lower():
            destination_language = get_voice_input("Please speak the destination language you want to translate to:", recognizer, engine)
            if destination_language:
                input_text = get_voice_input("Please speak the text you want to translate:", recognizer, engine)
                if input_text:
                    translate(input_text, destination_language, engine)
        elif "date" in text.lower():
            date_time = get_date_time()
            print("Current Date and Time:", date_time)
            engine.say("The current date and time is " + date_time)
            engine.runAndWait()
        elif "introduce yourself" in text.lower() or "yourself" in text.lower():
            introduce(engine)
        elif "play" in text.lower():
            play(text, engine)
        elif "who is " in text.lower():
            person_name = text.lower().replace("who is ", "")
            get_wikipedia_summary(person_name, engine)
        elif "joke" in text.lower():
            joke = pyjokes.get_joke()
            print("Joke:", joke)
            engine.say(joke)
            engine.runAndWait()
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio. Please try again.")
        engine.say("Sorry, I could not understand the audio. Please try again.")
        engine.runAndWait()
        break
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        engine.say("Could not request results from Google Speech Recognition service. Please try again.")
        engine.runAndWait()
        break
