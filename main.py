import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import openai  # Correct OpenAI import
import os

# Initialize recognizer and pyttsx3 engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# API keys (you can also use environment variables for security)
newsapi_key = "b8c65c24df624df3943fbe2634a068d3"
openai.api_key = "sk-x11jUhhrDC4c3wGqch7869y8PxrMmt-rf7jAqzUI8dT3BlbkFJTWF-75Qm38FylRqcH3rGLAkk4WGRNuHAAqW5w9uWUA"

# Function to make Jarvis speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to process OpenAI requests
def ai_process(command):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Assistant."},
                {"role": "user", "content": command}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"

# Function to fetch and read news headlines
def fetch_news():
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi_key}"
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            if articles:
                speak("Here are the top news headlines:")
                for article in articles[:5]:  # Read only the top 5 headlines
                    speak(article['title'])
            else:
                speak("Sorry, I couldn't find any news right now.")
        else:
            speak("Sorry, I couldn't fetch the news.")
    except Exception as e:
        speak(f"There was an error fetching the news: {e}")

# Function to process user commands
def process_command(command):
    command = command.lower()

    if "open google" in command:
        webbrowser.open("https://google.com")
        speak("Opening Google.")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
        speak("Opening Facebook.")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube.")
    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")
        speak("Opening LinkedIn.")
    elif command.startswith("play"):
        song = command.split(" ")[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
            speak(f"Playing {song}.")
        else:
            speak("Sorry, I couldn't find that song.")
    elif "news" in command:
        fetch_news()
    else:
        # Let OpenAI handle other requests
        output = ai_process(command)
        speak(output)

# Main function to listen for commands
def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        speak("I am listening, please say 'Jarvis' to activate.")
        
        while True:
            try:
                print("Listening for 'Jarvis' wake word...")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                wake_word = recognizer.recognize_google(audio).lower()

                if wake_word == "jarvis":
                    speak("Yes, I'm here.")
                    print("Listening for command...")
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    print(f"Command: {command}")
                    process_command(command)

            except sr.UnknownValueError:
                speak("Sorry, I didn't catch that.")
            except sr.RequestError as e:
                speak(f"Network error: {e}")
            except Exception as e:
                speak(f"An error occurred: {e}")

# Entry point of the program
if __name__ == "__main__":
    speak("Initializing Jarvis")
    listen()
