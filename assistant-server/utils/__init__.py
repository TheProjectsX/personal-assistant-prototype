import re
from . import command_detector as cmd
from . import parsers


# Get response data
def getResponse(text: str, arguments: str = {}) -> dict:
    cleaned_text = re.sub(r"[^\w\s]", "", text.lower())

    command = cmd.detect_command(text)
    func = getattr(parsers, command)

    response = func(cleaned_text, arguments)
    return response
