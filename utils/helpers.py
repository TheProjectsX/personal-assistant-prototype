"""
Here are some helper functions
"""

# Flatten the Given nester list and return only unique items
import re
import langcodes
import requests


def flatten_and_unique(nested_list: list) -> list:
    unique_items = set()

    def flatten(item):
        if isinstance(item, list):
            for sub_item in item:
                flatten(sub_item)
        else:
            unique_items.add(item)

    flatten(nested_list)
    return list(unique_items)


# Cleaned Text:: Remove every Item from a text from a given List
def clean_text(text: str, items: list) -> str:
    cleanedText = text
    for item in items:
        cleanedText = cleanedText.replace(item, "", 1)

    return cleanedText.strip()


# Parse the YouTube Video link from a text
def parse_youtube_url(topic: str):
    """Will play video on following topic, takes a
    bout 10 to 15 seconds to load"""
    url = "https://www.youtube.com/results?q=" + topic

    count = 0

    response = requests.get(url)

    data = response.content
    data = str(data)

    contents = data.split('"')
    for content in contents:
        count += 1
        if content == "WEB_PAGE_TYPE_WATCH":
            break

    if contents[count - 5] == "/results":
        return None

    match = re.search(r"v=([\w-]+)", contents[count - 5])
    if match:
        return f"https://www.youtube.com/watch?v={match.group(1)}"

    return None


# Detect Languages from a text
def detect_language_words(text: str) -> list:
    splitted_text = text.split(" ")
    languages = []

    for word in splitted_text:
        try:
            lang = langcodes.find(word)
            if lang.is_valid():
                languages.append(
                    {"name": lang.language_name(), "code": lang.language, "word": word}
                )
        except Exception as e:
            pass

    return languages
