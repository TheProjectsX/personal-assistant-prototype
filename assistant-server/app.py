from flask import Flask, request
import utils

# Setup App
app = Flask(__name__)


# Test route
@app.route("/")
def home():
    return {"success": True}


# Assistant Route
@app.route("/assistant", methods=["POST"])
def assistant():
    text = request.json.get("text", "")
    arguments = request.json.get("arguments", {})
    response = utils.getResponse(text, arguments)

    return response


# Start the app
if __name__ == "__main__":
    app.run(debug=True)
