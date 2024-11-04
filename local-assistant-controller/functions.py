from typing import Union
import webbrowser
import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 150)


# Utility Functions
# Speak


def speak(text: str):
    if text == "":
        return
    print("Speaking:", text)
    engine.say(text)
    engine.runAndWait()


### Control Functions


# Play Music on YouTube
def play_music(arguments: dict, text: str = ""):
    name: Union[str, None] = arguments.get("name")
    type: Union[str, None] = arguments.get("type", "direct")
    youtube_url: Union[str, None] = arguments.get("youtube_url")
    speak(text)

    if type == "custom":
        if youtube_url:
            webbrowser.open(youtube_url)
