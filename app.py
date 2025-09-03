from flask import Flask, render_template_string
import paho.mqtt.client as mqtt

BROKER = "yamanote.proxy.rlwy.net"   # ganti sesuai host Railway broker kamu
PORT = 55931                         # port broker
TOPIC = "telegram/input"

app = Flask(__name__)
latest_message = "Belum ada pesan"

# MQTT setup
def on_connect(client, userdata, flags, rc):
    print("Connected MQTT:", rc)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    global latest_message
    latest_message = msg.payload.decode()
    print("New message:", latest_message)

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(BROKER, PORT, 60)
mqtt_client.loop_start()

@app.route("/")
def index():
    html = f"""
    <html>
      <head><title>Telegram → MQTT → Web</title></head>
      <body style="font-family:sans-serif;text-align:center;margin-top:50px;">
        <h2>Pesan terbaru dari Telegram:</h2>
        <h1 style="color:green;">{latest_message}</h1>
      </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Railway inject PORT
    app.run(host="0.0.0.0", port=port, debug=False)

