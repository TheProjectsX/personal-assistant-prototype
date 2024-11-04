import requests
import functions as fns

SERVER_URL = "http://localhost:5000"


while True:
    try:
        try:
            text = input("\nEnter Text:> ")
        except KeyboardInterrupt:
            break

        if not "pluto" in text.lower().split(" ")[:3]:
            continue

        json = {"text": text.replace("pluto", "", 1).strip()}

        response: dict = requests.post(f"{SERVER_URL}/assistant", json=json).json()

        if response.get("command") == "speak":
            fns.speak(response.get("text"))
        elif response.get("command") == "run_function":
            func = getattr(fns, response.get("function"))
            func(response.get("arguments", {}), text=response.get("text", ""))
        else:
            print(response)

    except Exception as e:
        print(e)
        fns.speak("Something went wrong!")
