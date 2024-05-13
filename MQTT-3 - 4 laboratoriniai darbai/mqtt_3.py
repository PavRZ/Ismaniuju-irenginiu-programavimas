import paho.mqtt.client as mqtt
import time

data = '{"firstName": "tester", "lastName": "tester", "city": "Vilnius"}'

def connect_broker(broker_address, client_name):
    client = mqtt.Client(client_name)
    client.connect(broker_address)
    time.sleep(1)
    client.loop_start()

    return client

if __name__ == "__main__":
    server = "broker.emqx.io"
    client_name = "zmogus"
    client = connect_broker(server, client_name)
    try:
        while True:
            message = input('Iveskite siuntimo raktazodi:')
            if message == '1':
                client.publish("json/1ldJSON",data)
                print("Pranešimas išsiustas")
            else:
                print("Blogas raktazodis") 
    except KeyboardInterrupt:
        client.disconnect()
        client.Loop_stop()