"""
Structure of Command Intents:

- min_match: Minimum match count (is not in operation)
- required_keywords: the required keywords which must be in the Command in order to go farther
- command: the command name, duh!
- keywords:
    - list -> items :-> required
    - list -> list -> items :-> required with "OR". Any one of the Item must be matched
    - list -> list -> list -> items :-> required with "AND". All the items must match

    Flow:
        required
            required with or -> ["a" or "b" or ["c", "d"]]
                required with and -> ["c" and "d"]

"""

# Commands - Will be placed in another file
CommandIntents = [
    {
        "min_match": 2,
        "required_keywords": ["time"],
        "keywords": [["what", "tell", ["can you", "tell"]], "time"],
        "command": "current_time",
    },
    {
        "min_match": 2,
        "required_keywords": ["weather"],
        "keywords": [["what", "check", ["show", "display"]], "weather"],
        "command": "current_weather",
    },
    {
        "min_match": 2,
        "required_keywords": ["date"],
        "keywords": [["what", "tell", ["can you", "please"]], "date"],
        "command": "current_date",
    },
    {
        "min_match": 2,
        "required_keywords": ["music"],
        "keywords": [["play", "start", ["some", "the"]], "music"],
        "command": "play_music",
    },
    {
        "min_match": 2,
        "required_keywords": ["news"],
        "keywords": [["tell", "show", ["what", "is"], ["latest", "today"]], "news"],
        "command": "show_news",
    },
    {
        "min_match": 2,
        "required_keywords": ["browser"],
        "keywords": [["open", "launch", ["start", "initiate"]], "browser"],
        "command": "open_browser",
    },
    {
        "min_match": 2,
        "required_keywords": ["reminder"],
        "keywords": [["set", "create", ["add", "new"]], "reminder"],
        "command": "set_reminder",
    },
    {
        "min_match": 2,
        "required_keywords": ["alarm"],
        "keywords": [["set", "create", ["add", "new"]], "alarm"],
        "command": "set_alarm",
    },
    {
        "min_match": 2,
        "required_keywords": ["location"],
        "keywords": [["find", "show", "navigate"], "location"],
        "command": "open_map",
    },
    {
        "min_match": 2,
        "required_keywords": ["calculator"],
        "keywords": [["open", "launch", ["start", "run"]], "calculator"],
        "command": "open_calculator",
    },
    {
        "min_match": 2,
        "required_keywords": ["joke"],
        "keywords": [["tell", "say", ["funny", "humorous"]], "joke"],
        "command": "tell_joke",
    },
    {
        "min_match": 2,
        "required_keywords": ["translate"],
        "keywords": [["translate", "interpret"], "text"],
        "command": "translate_text",
    },
    {
        "min_match": 2,
        "required_keywords": ["location"],
        "keywords": [["where", "locate"], "I"],
        "command": "get_location",
    },
]
