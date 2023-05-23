import RPi.GPIO as GPIO
import config

def idle():
    GPIO.output(config.LED_FRONT_PIN, False)
    GPIO.output(config.LED_BACK_PIN, False)
    GPIO.output(config.LED_LEFT_PIN, False)
    GPIO.output(config.LED_RIGHT_PIN, False)


def forward():
    GPIO.output(config.LED_FRONT_PIN, True)
    GPIO.output(config.LED_BACK_PIN, False)
    GPIO.output(config.LED_LEFT_PIN, False)
    GPIO.output(config.LED_RIGHT_PIN, False)


def backward():
    GPIO.output(config.LED_FRONT_PIN, False)
    GPIO.output(config.LED_BACK_PIN, True)
    GPIO.output(config.LED_LEFT_PIN, False)
    GPIO.output(config.LED_RIGHT_PIN, False)


def turn_left():
    GPIO.output(config.LED_FRONT_PIN, False)
    GPIO.output(config.LED_BACK_PIN, False)
    GPIO.output(config.LED_LEFT_PIN, True)
    GPIO.output(config.LED_RIGHT_PIN, False)