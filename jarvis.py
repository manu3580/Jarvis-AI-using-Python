import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import pyjokes

engine = pyttsx3.init('espeak')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    print(f"Jarvis: {audio}")
    engine.say(audio)
    engine.runAndWait()

def wish_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("Hello! I am Jarvis. How can I assist you today?")

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
    except Exception:
        print("Say that again please...")
        return "None"
    return query.lower()

def send_email(to, content):
    # Replace with your email credentials before using
    your_email = "your_email@gmail.com"
    your_password = "your_password"
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(your_email, your_password)
        server.sendmail(your_email, to, content)
        server.close()
        speak("Email has been sent successfully.")
    except Exception as e:
        print(e)
        speak("Sorry, I am unable to send the email right now.")

if __name__ == "__main__":
    wish_me()
    while True:
        query = take_command()

        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
            except Exception:
                speak("Sorry, I couldn't find any information on that topic.")

        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("https://youtube.com")

        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("https://google.com")

        elif 'open github' in query:
            speak("Opening GitHub")
            webbrowser.open("https://github.com")

        elif 'time' in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {str_time}")

        elif 'date' in query:
            today = datetime.date.today()
            speak(f"Today's date is {today.strftime('%B %d, %Y')}")

        elif 'joke' in query:
            speak(pyjokes.get_joke())

        elif 'email' in query:
            try:
                speak("What should I say?")
                content = take_command()
                speak("Please tell me the receiver's email address.")
                to = input("Enter receiver email: ")
                send_email(to, content)
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't send your email.")

        elif 'exit' in query or 'quit' in query or 'stop' in query:
            speak("Goodbye! Have a nice day!")
            break

        else:
            speak("I'm sorry, I didn't understand that command.")
