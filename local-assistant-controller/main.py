import requests
import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)


SERVER_URL = "http://localhost:5000"


def speak(text):
    print("Speaking:", text)
    engine.say(text)
    engine.runAndWait()


while True:
    try:
        try:
            text = input("\nEnter Text:> ")
        except KeyboardInterrupt:
            break

        if not "pluto" in text.lower().split(" ")[:3]:
            continue

        json = {"text": text.replace("pluto", "", 1).strip()}

        response = requests.post(f"{SERVER_URL}/assistant", json=json).json()

        if response.get("command") == "speak":
            speak(response.get("text"))
        else:
            print(response)
    except Exception as e:
        print(e)
        speak("Something went wrong!")
