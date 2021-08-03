import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import pyaudio
import string
import random
from bs4 import BeautifulSoup
import requests
from sys import exit

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 175)


# Speak the content using `pyttsx3` library.
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am your personal Desktop Assistant. Please tell me how may I help you? ")


# Takes microphone input from the user and returns string output.
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1       # Seconds of non-speaking audio before a phrase is considered complete.
        r.energy_threshold = 600    # Minimum audio energy to consider for recording
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")

    except Exception:
        print("Say that again please...")
        return "None"
    return query


# Performs a google search and returns the result.
def google(query):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    query = query.replace(" ", "+")
    try:
        url = f"https://www.google.com/search?q={query}&oq={query}&aqs=chrome..69i57j46j69i59j35i39j0j46j0l2.4948j0j7&sourceid=chrome&ie=UTF-8"
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
    except:
        print("Make sure you have a internet connection")
    try:
        try:
            ans = soup.select(".RqBzHd")[0].getText().strip()

        except:
            try:
                title = soup.select(".AZCkJd")[0].getText().strip()
                try:
                    ans = soup.select(".e24Kjd")[0].getText().strip()
                except:
                    ans = ""
                ans = f"{title}\n{ans}"

            except:
                try:
                    ans = soup.select(".hgKElc")[0].getText().strip()
                except:
                    ans = soup.select(".kno-rdesc span")[0].getText().strip()

    except:
        ans = "Can't find on Google!!!"
    return ans


if __name__ == "__main__":
    wishMe()
    while True:        # Run forever
    # if 1:            # Run once
        query = takeCommand().lower()

        if "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=3)
            speak("According to Wikipedia")
            print(f"{results}\n")
            speak(results)

        elif "youtube" in query:
            webbrowser.open("youtube.com")

        elif "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif "open code" in query:
            codePath = "C:\\Program Files\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif "password" in query:
            s1 = string.ascii_lowercase
            s2 = string.ascii_uppercase
            s3 = string.digits
            s4 = string.punctuation
            speak("Enter password length")
            pass_len = int(input("Enter password length: "))
            s = []
            s.extend(list(s1))
            s.extend(list(s2))
            s.extend(list(s3))
            s.extend(list(s4))
            print("Password: ", end=" ")
            print("".join(random.sample(s, pass_len)))
            speak("Strong password generated: ")

        elif "google" in query:
            speak("Searching Google...")
            query = query.replace("google", "")
            result = google(query)
            print(result, "\n")
            speak(result)
        elif "exit" or "close" or "shutdown" in query:
            print("Shutting down....\n")
            sys.exit()
