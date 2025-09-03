from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello Railway, Flask is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))   # Ambil PORT dari env Railway
    app.run(host="0.0.0.0", port=port, debug=True)
