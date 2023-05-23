import RPi.GPIO as GPIO
import time

class UltrasonSensor:
    def __init__(self, trig_pin, echo_pin):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def measure_distance(self):
        GPIO.output(self.trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, False)

        start_time = time.time()
        stop_time = time.time()

        while GPIO.input(self.echo_pin) == 0:
            start_time = time.time()

        while GPIO.input(self.echo_pin) == 1:
            stop_time = time.time()

        elapsed_time = stop_time - start_time
        distance = (elapsed_time * 34300) / 2
        return distance

    def measure_speed(self, delay=0.1):
        distance1 = self.measure_distance()
        time.sleep(delay)
        distance2 = self.measure_distance()

        velocity = abs(distance2 - distance1) / delay
        return velocity

    def __del__(self):
        GPIO.cleanup()
