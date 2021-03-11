import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import pyjokes
import wikipedia
import smtplib
from test import contacts
from test import to

listener = sr.Recognizer()
engine = pyttsx3.init('sapi5')

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.say("hello! I am Silvana, What can I do for you?")
engine.runAndWait()


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:

            print("listening.....")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'silvana' in command:
                command = command.replace('silvana', '')
                print(command)

    except:
        print("error")
        pass

    return command


def send_email():
    talk("send email to whom?")
    receiver = take_command()
    talk(f"okay! you want to send email to {receiver}")
    talk("tell me the message!")
    message = take_command()
    print(message)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('vachtani02@gmail.com', '**********')
    server.sendmail('vachtani02@gmail.com', contacts[receiver], message)
    server.close()


def run_silvana():
    command = take_command()
    print(command)
    if 'play' in command:
        command = command.replace('play', "")
        talk('playing ' + command)
        pywhatkit.playonyt(command)
    elif 'time' in command:
        time1 = datetime.datetime.now().strftime("%I:%M %p")
        talk("current time is " + time1)
    elif "who is" in command:
        command = command.replace('who is', '')
        try:
            results = wikipedia.summary(command, sentences=3)
            if results:
                talk(results)
            else:
                talk("sorry! I couldn't find any results for" + command)
        except Exception as e:
            talk("Sorry! I could'nt find any results for " + command)

    elif "joke" in command:
        talk(pyjokes.get_joke('en', 'all'))
    elif "whatsapp" in command:
        talk("okay! so whom do you want to send whatsapp message?")
        to1 = take_command()
        talk(f"sending to {to1}")
        talk("tell the whatsapp text!")
        wp_message = take_command()
        pywhatkit.sendwhatmsg(to[to1], wp_message, datetime.datetime.now().hour, datetime.datetime.now().minute + 2)
    elif "send email" in command:
        try:
            send_email()
        except Exception as e:
            print(e)
    else:
        talk("sorry! I couldn't understand that")


while True:
    run_silvana()
