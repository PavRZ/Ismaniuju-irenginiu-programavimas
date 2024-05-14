from flask import Flask, render_template
import requests
import json
from flask_mqtt import Mqtt

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'broker.mqttdashboard.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 10
app.config['MQTT_TLS_ENABLED'] = False

topic = 'api/test1'
mqtt_client = Mqtt(app)

faktu_kiekis = 2

@app.route('/')
def katinas():
    url = f"https://cat-fact.herokuapp.com/facts/random?amount={faktu_kiekis}"
    requested_data = requests.get(url)
    requested_data_json_format = requested_data.json()

    print (requested_data_json_format)
    
    save_path = "api.json"
    with open(save_path, 'w') as f:
        json.dump(requested_data_json_format, f)

    mqtt_client.publish(topic, json.dumps(requested_data_json_format))

    print(type(requested_data_json_format))
    
    return render_template('index.html', data=requested_data_json_format)

@app.route('/get-facts')
def faktu_gavimas():
    url = f"https://cat-fact.herokuapp.com/facts/random?amount={faktu_kiekis}"
    requested_data = requests.get(url)
    requested_data_json_format = requested_data.json()
    data = requested_data_json_format
    
    mqtt_client.publish(topic, json.dumps(requested_data_json_format))

    return data

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80)
