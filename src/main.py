import base64
import time
import threading
import os
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import config
import variables
import ultrasonSensor
from ledControl import Led
import sys
from PIL import Image
import subprocess
import detect_from_image
sys.path.append("/home/pi/Vision-car/vision_car_model/saved_model")

# GPIO Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
led_front = Led(config.LED_FRONT_PIN)
led_back = Led(config.LED_BACK_PIN)
led_left = Led(config.LED_LEFT_PIN)
led_right = Led(config.LED_RIGHT_PIN)

# Ultrason Instance
ultrasonFront = ultrasonSensor.UltrasonSensor(config.TRIG_FRONT_PIN, config.ECHO_FRONT_PIN)
ultrasonBack = ultrasonSensor.UltrasonSensor(config.TRIG_BACK_PIN, config.ECHO_BACK_PIN)

# MQTT Config
# Fonction pour la publication MQTT
def publish_mqtt(topic, message):
    mqtt_client.publish(topic, message)

# Fonction pour la lecture des messages MQTT
def on_message(client, userdata, msg):
    global ultrasonBack
    global led_front, led_back, led_left, led_right

    message = msg.payload.decode()
    topic = msg.topic

    if topic == "mode":
        if message == "manuel":
            direction = userdata.get("direction", None)

            if direction == "front":
                led_front.on()
                led_back.off()
                led_left.off()
                led_right.off()
            elif direction == "back":
                led_front.off()
                led_back.on()
                led_left.off()
                led_right.off()
            elif direction == "left":
                led_front.off()
                led_back.off()
                led_left.on()
                led_right.off()
            elif direction == "right":
                led_front.off()
                led_back.off()
                led_left.off()
                led_right.on()
            else:
                led_front.off()
                led_back.off()
                led_left.off()
                led_right.off()

        elif message == "automatique":
            led_front.off()
            led_back.off()
            led_left.off()
            led_right.off()

    elif topic == "direction":
        userdata["direction"] = message

# Initialisation du client MQTT
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message

# Connexion au broker MQTT
mqtt_client.connect(variables.HOST, variables.PORT)

# Souscription aux topics MQTT
for topic in variables.topicsSubscribed:
    mqtt_client.subscribe(topic)

# Fonction pour la récupération des mesures des capteurs
def get_sensor_measurements():
    while True:
        distance_avant = ultrasonFront.measure_distance()
        distance_arrière = ultrasonBack.measure_distance()
        vitesse_avant = ultrasonFront.measure_speed()
        vitesse_arrière = ultrasonBack.measure_speed()

        publish_mqtt(variables.topicsPublished[0], str(distance_avant))
        publish_mqtt(variables.topicsPublished[1], str(vitesse_avant))
        publish_mqtt(variables.topicsPublished[2], str(distance_arrière))
        publish_mqtt(variables.topicsPublished[3], str(vitesse_arrière))


# Fonction pour la capture d'image et la détection d'objets
def capture_and_detect():
    while True:
        os.system("libcamera-jpeg -o images/img_camera.jpg -t 10 --width 640 --height 480")
        # Appel de la fonction de détection d'objets
        detect_from_image.perform_object_detection("images/img_camera.jpg",
                                 "images/detection_output{}.jpg",
                                 "../vision_car_model/saved_model",
                                 "../vision_car_model/labelmap.pbtxt")

        # Publication du résultat de la détection sur MQTT
        img_object_detected_path = "images/detection_output0.jpg"
        # Ouvrir l'image avec PIL
        image = Image.open(img_object_detected_path)

        # Convertir l'image en format binaire
        with open(img_object_detected_path, "rb") as f:
            image_data = f.read()

        # Convertir l'image binaire en base64
        image_base64 = base64.b64encode(image_data).decode("utf-8")

        # Publier l'image sur MQTT
        publish_mqtt(variables.topicsPublished[4], image_base64)


# Fonction pour exécuter Node-RED
def start_node_red():
    subprocess.run(["node-red"])

# Fonction pour le séquencage de clignotement des LEDs
def blink_leds_sequence():
    led_front.off()
    led_back.off()
    led_left.off()
    led_right.off()

    for _ in range(10):
        led_front.toggle()
        led_back.toggle()
        led_left.toggle()
        led_right.toggle()
        time.sleep(0.5)

    led_front.off()
    led_back.off()
    led_left.off()
    led_right.off()

# Création des threads pour l'exécution parallèle
capture_thread = threading.Thread(target=capture_and_detect)
sensor_thread = threading.Thread(target=get_sensor_measurements)
node_red_thread = threading.Thread(target=start_node_red)
blink_thread = threading.Thread(target=blink_leds_sequence)

# Démarrage des threads
capture_thread.start()
sensor_thread.start()
node_red_thread.start()
blink_thread.start()

# Attendre que le séquencage de clignotement des LEDs soit terminé avant de continuer
blink_thread.join()

# Boucle principale
while True:
    # Écoute des messages MQTT en arrière-plan
    mqtt_client.loop_start()

    # Contrôle automatique
    distance_avant = ultrasonFront.measure_distance()

    if distance_avant > 20:
        led_front.on()
        led_back.off()
        led_left.off()
        led_right.off()
    else:
        led_front.off()
        led_back.off()
        led_left.off()
        led_right.off()

    # Pause pour éviter une consommation excessive du processeur
    time.sleep(0.1)

    # Arrêt de l'écoute des messages MQTT
    mqtt_client.loop_stop()
