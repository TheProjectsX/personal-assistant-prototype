"""
This file contains the Functions which will parse the given text and make response for the client device.
- Either it will parse and return response.
- Or parse and create command and return command response
"""

from datetime import datetime
import pytz

# import .ResponseCodes as res_codes
from . import ResponseCodes as res_codes
from .COMMANDS import CommandIntents
from . import helpers
import requests
from googletrans import Translator


# Format to Current Time
def current_time(text: str = "", arguments: dict = {}) -> dict:
    timezone = pytz.timezone(arguments.get("timezone", "Asia/Dhaka"))

    current_time = datetime.now(timezone)
    hour = current_time.hour

    if 5 <= hour < 12:
        greeting = "Good morning, sir!"
    elif 12 <= hour < 18:
        greeting = "Good afternoon, sir!"
    else:
        greeting = "Good evening, sir!"

    formatted_time = current_time.strftime(f"{greeting} It's %I:%M %p")
    response = {"command": res_codes.SPEAK, "text": formatted_time}

    return response


# Format to Current Date
def current_date(text: str = "", arguments: dict = {}) -> dict:
    timezone = pytz.timezone(arguments.get("timezone", "Asia/Dhaka"))

    current_time = datetime.now(timezone)
    greeting = "Hello, sir!"

    formatted_time = current_time.strftime(f"{greeting} Today is %A, %B %d, %Y")
    response = {"command": res_codes.SPEAK, "text": formatted_time}

    return response


# Current Weather
def current_weather(text: str = "", arguments: dict = {}) -> dict:
    location = arguments.get("location", "Rangpur,BD")

    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={location}&APPID=43d5939ed78fea35f571312a7825b5c2"
    ).json()

    location = response["name"]
    description = response["weather"][0]["description"].capitalize()
    temp_celsius = round(
        response["main"]["temp"] - 273.15, 1
    )  # Convert from Kelvin to Celsius
    humidity = response["main"]["humidity"]
    wind_speed = response["wind"]["speed"]
    sunrise = datetime.fromtimestamp(response["sys"]["sunrise"]).strftime("%I:%M %p")
    sunset = datetime.fromtimestamp(response["sys"]["sunset"]).strftime("%I:%M %p")

    response = {
        "command": res_codes.SPEAK,
        "text": (
            f"The weather in {location} is currently {description} with a temperature of {temp_celsius}°C. "
            f"Humidity is at {humidity}% and wind speed is {wind_speed} m/s. "
            f"Sunrise was at {sunrise} and sunset will be at {sunset}."
        ),
    }

    return response


# Play Music
def play_music(text: str, arguments: dict = {}) -> dict:
    intent: dict = [x for x in CommandIntents if x.get("command") == "play_music"][0]
    keywords: list = intent.get("keywords")

    cleanedText = helpers.clean_text(text, items=helpers.flatten_and_unique(keywords))
    if cleanedText in intent.get("stop_words"):
        cleanedText = ""

    if cleanedText == "":
        response = {"command": res_codes.PLAY_MUSIC, "arguments": {"type": "any"}}
    else:
        youtube_url = helpers.parse_youtube_url(cleanedText)
        response = {
            "command": res_codes.RUN_FUNCTION,
            "function": "play_music",
            "text": f"Playing {cleanedText}",
            "arguments": {
                "type": "custom",
                "name": cleanedText,
                "youtube_url": youtube_url,
            },
        }

    return response


# Open Browser
def open_browser(text: str, arguments: dict = {}) -> dict:
    response = {
        "command": res_codes.RUN_FUNCTION,
        "text": "Opening Browser",
        "function": "open_browser",
    }

    return response


# Translate Text
def translate_text(text: str, arguments: dict = {}) -> dict:
    intent: dict = [x for x in CommandIntents if x.get("command") == "translate_text"][
        0
    ]
    keywords: list = intent.get("keywords")
    cleanedText = helpers.clean_text(text, items=helpers.flatten_and_unique(keywords))

    languages: list = helpers.detect_language_words(cleanedText)

    src, dest = "auto", "en"
    if len(languages) == 1:
        dest = languages[0].get("code")
    elif len(languages) > 1:
        src = languages[0].get("code")
        dest = languages[1].get("code")

    cleanedText = helpers.clean_text(
        cleanedText, items=[x.get("word") for x in languages[:2]]
    )

    translator = Translator()
    translated = translator.translate(text=cleanedText, src=src, dest=dest)
    translated_text = translated.text

    response = {"command": res_codes.SPEAK, "text": translated_text}

    return response


# Realtime Translate
def translate_realtime(text: str, arguments: dict = {}) -> dict:
    intent: dict = [
        x for x in CommandIntents if x.get("command") == "translate_realtime"
    ][0]
    keywords: list = intent.get("keywords")
    cleanedText = helpers.clean_text(text, items=helpers.flatten_and_unique(keywords))

    languages: list = helpers.detect_language_words(cleanedText)

    src, dest = "auto", "en"
    if len(languages) == 1:
        dest = languages[0].get("code")
    elif len(languages) > 1:
        src = languages[0].get("code")
        dest = languages[1].get("code")

    response = {
        "command": res_codes.RUN_FUNCTION,
        "function": "translate_realtime",
        "arguments": {
            "src": src,
            "dest": dest,
        },
    }

    return response


# Test Run
if __name__ == "__main__":
    print(translate_realtime("translate realtime to japaneese"))
