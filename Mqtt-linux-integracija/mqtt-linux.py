import json
import paho.mqtt.client as mqtt

# MQTT brokerio nustatymai
mqtt_broker_address ="broker.mqttdashboard.com"
mqtt_port = 1883
mqtt_topic = "hello/world15"

data = {
    "glossary": {
        "title": "example glossary",
		"GlossDiv": {
            "title": "S",
			"GlossList": {
                "GlossEntry": {
                    "ID": "SGML",
					"SortAs": "SGML",
					"GlossTerm": "Standard Generalized Markup Language",
					"Acronym": "SGML",
					"Abbrev": "ISO 8879:1986",
					"GlossDef": {
                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
						"GlossSeeAlso": ["GML", "XML"]
                    },
					"GlossSee": "markup"
                }
            }
        }
    }
}

# Funkcija, kuri išsaugo JSON failą su nurodytu turiniu
def save_json_to_file(json_content):
    file_path = "/tmp/sample.json"  # Galite pakeisti norimu failo pavadinimu ir keliu

    with open(file_path,"w", encoding="utf-8") as file:
        json.dump(json_content, file)

# Funkcija, kuri apdoroja gautus MQTT pranešimus
def on_message(client, userdata, message):
    try:
        # reboot_with_password()
        payload = str(message.payload.decode("utf-8"))
        if payload == "raktazodis":     # Checking whether a keyword sent to MQTT to save JSON is correct
            save_json_to_file(data)
            mqtt_client.publish("hello/world16", f"JSON failas sukurtas {data}")
            
        else:
            mqtt_client.publish("hello/world16", "JSON failas nesukurtas, ivedete bloga raktazodi")
    except Exception as e:
        print("Klaida apdorojant pranešimą:", e)


# Sukuriamas MQTT klientas
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message

# Prisijungiama prie MQTT brokerio
mqtt_client.connect(mqtt_broker_address, mqtt_port)

# Prenumeruojamas temos, iš kurios bus gauti pranešimai
mqtt_client.subscribe(mqtt_topic)

# Paleidžiama MQTT kliento gija
mqtt_client.loop_forever()