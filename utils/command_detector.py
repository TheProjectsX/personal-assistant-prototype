import re
from COMMANDS import CommandIntents

"""
Intents Keywords List Logic:
- list -> items :-> required
- list -> list -> items :-> required with "OR". Any one of the Item must be matched
- list -> list -> list -> items :-> required with "AND". All the items must match

Flow:
    required
        required with or -> ["a" or "b" or ["c", "d"]]
            required with and -> ["c" and "d"]
"""


def match_word(tokens, word, start_index):
    for i in range(start_index, len(tokens)):
        if tokens[i] == word:
            return i + 1
    return -1


def get_next_index(tokens, item, current_index):
    for i in range(current_index, len(tokens)):
        if tokens[i] == item or (
            isinstance(item, list) and all(sub in tokens for sub in item)
        ):
            return i + 1
    return current_index


def handle_nested_list(tokens, subkeywords, start_index):
    found = any(
        element in tokens[start_index:]
        for element in subkeywords
        if not isinstance(element, list)
    )

    if found:
        return True

    for and_required in (item for item in subkeywords if isinstance(item, list)):
        joined_tokens = " ".join(tokens[start_index:])
        if all(
            word
            in (joined_tokens if re.search(r"\w \w", word) else tokens[start_index:])
            for word in and_required
        ):
            return True

    return False


# Match the keywords and do required operations for nested keywords
def match_keywords(tokens, keywords):
    index = 0

    for item in keywords:
        if isinstance(item, list):
            if not handle_nested_list(tokens, item, index):
                return False
            index = get_next_index(tokens, item, index)
        else:
            index = match_word(tokens, item, index)
            if index == -1:
                return False
    return True


# Find the Command from given Text
def detect_command(text: str):
    # Remove Punctuations
    cleaned_text = re.sub(r"[^\w\s]", "", text.lower())
    splitted_text = cleaned_text.split(" ")

    detected_command = None

    for intent in CommandIntents:
        if not any(kw in splitted_text for kw in intent.get("required_keywords")):
            continue

        if match_keywords(splitted_text, intent.get("keywords")):
            detected_command = intent.get("command")

    return detected_command


if __name__ == "__main__":
    pass
