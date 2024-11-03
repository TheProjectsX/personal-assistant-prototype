import re
from typing import Union
from fuzzywuzzy import fuzz
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


# Fuzzy Wuzzy match Commands
def match_command(tokens: list, keywords: list, min_match: int) -> bool:

    # Check fuzzy matching for broader keywords list
    match_count = 0
    for keyword_group in keywords:
        if isinstance(keyword_group, list):
            # OR condition: find the best fuzzy match in the group
            group_match = any(
                fuzz.token_set_ratio(" ".join(tokens), option) >= 80
                for option in keyword_group
            )
            if group_match:
                match_count += 1
        else:
            # Individual keywords
            if fuzz.token_set_ratio(" ".join(tokens), keyword_group) >= 80:
                match_count += 1

    # Final command matching check
    if match_count >= min_match:
        return True


# Find the Command from given Text
def detect_command(text: str) -> Union[str, None]:
    # Remove Punctuations
    cleaned_text = re.sub(r"[^\w\s]", "", text.lower())
    splitted_text = cleaned_text.split(" ")

    detected_command = None

    for intent in CommandIntents:
        if (len(intent.get("required_keywords")) > 0) and (
            not any(kw in splitted_text for kw in intent.get("required_keywords"))
        ):
            continue

        if match_command(
            splitted_text, intent.get("keywords"), intent.get("min_match")
        ):
            detected_command = intent.get("command")
            break

    return detected_command


if __name__ == "__main__":
    while True:
        try:
            text = input("\nText:> ")
            print("Command:", detect_command(text))
        except KeyboardInterrupt:
            break
