from nordpool import nordpool
from flask import Flask, render_template
from flask_mqtt import Mqtt

app = Flask(__name__)
# MQTT configuration
app.config['MQTT_BROKER_URL'] = 'broker.mqttdashboard.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 10
app.config['MQTT_TLS_ENABLED'] = False

mqtt_client = Mqtt(app)

topic_sub = 'hello/world15'
topic_pub = 'hello/world16'

# Function that shows what it does on MQTT broker connection
@mqtt_client.on_connect()
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        mqtt_client.subscribe(topic_sub)
    else:
        print(f"Failed to connect, return code {rc}")

# Functions that executes code upon message arrival in MQTT sub topic (hello/world15)
@mqtt_client.on_message()
def on_message(client, userdata, message):
    global sent_message
    sent_message = nordpool()
    mqtt_client.publish(topic_pub, f"Pirma nuskaitytos lentelės eilutė {str(sent_message[0])}")

@app.route('/table')
def index():
    if sent_message:
        mqtt_client.publish(topic_pub, "Duomenys atvaizduoti FLASK Web lenteleje")
        return render_template('index.html', data=sent_message)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80)
