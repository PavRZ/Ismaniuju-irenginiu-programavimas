import paho.mqtt.client as mqtt
import json

MQTT_Topic = "api/test1"
mqttBroker ="broker.mqttdashboard.com"

def on_message(client, userdata, message):
    # print("received message: " ,str(message.payload.decode("utf-8")))
    if len(message.payload.decode("utf-8")) > 0:
        
        message_json = message.payload.decode("utf-8")
        json_data = json.loads(message_json)

        for item in json_data:
            text = item.get("text", "")
            if text:
                print("Extracted text:", text)
                # Publish the text to another topic
                content = f'GAVAU FAKTA APIE KATINA: {text}'
                client.publish("api/sub_response", str(content))
    
# client = mqtt.Client("1211213")
client = mqtt.Client()
client.connect(mqttBroker) 


client.subscribe(MQTT_Topic)
client.on_message=on_message
client.loop_forever() 
