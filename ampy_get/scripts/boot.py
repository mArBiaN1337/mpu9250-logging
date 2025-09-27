import json
from machine import Pin 
import micropython
#pyright: reportMissingImports=false

class BootConfig:
    # make the code below but in OOP form
    # pin numbers for the leds
    LED_YELLOW = 4
    LED_RED = 21
    LED_GREEN = 22
    LED_BLUE = 23

    # pin number for the data logging button and data led
    DATA_LOGGING_PIN = 34
    DATA_SEND_PIN = 35
    DATA_LED = 2

    DATA_LOGGING_BUTTON = Pin(DATA_LOGGING_PIN, Pin.IN)
    DATA_LED = Pin(DATA_LED, Pin.OUT)

    def __init__(self):
        self.leds = {
            "yellow": Pin(self.LED_YELLOW, Pin.OUT),
            "red": Pin(self.LED_RED, Pin.OUT),
            "green": Pin(self.LED_GREEN, Pin.OUT),
            "blue": Pin(self.LED_BLUE, Pin.OUT),
        }
        self.DATA_LED.value(0)  # turn off data led
        self.all_leds_off()

        self.led_startup_sequence(repeat_count=2, delay_time=0.2)
        ssid, password = self.get_credentials()
        conn_status = self.connect_wifi(ssid, password)
        assert conn_status, "Failed to connect to WiFi"
        self.DATA_LED.value(1)  # indicate wifi is active (led not blinking)

    # all leds on
    def all_leds_on(self):
        for led in self.leds.values():
            led.value(1)

    #turn all leds off
    def all_leds_off(self):
        for led in self.leds.values():
            led.value(0)

    # turn on yellow and then red and then green and then blue in sequence
    # add argument to how much times to repeat and the delay time
    def led_startup_sequence(self, repeat_count=1, delay_time=0.5):
        import time

        self.all_leds_off()

        # repeat the sequence
        for _ in range(repeat_count):
            for led in self.leds.values():
                led.value(1)
                time.sleep(delay_time)
                led.value(0)

        self.all_leds_off()
        time.sleep(delay_time)
        self.all_leds_on()
        time.sleep(delay_time)
        self.all_leds_off()

    # get ssid and password from secret.txt
    def get_credentials(self):
        try:
            with open("secret.txt", "r") as f:
                lines = f.readlines()
                ssid = lines[0].strip()
                password = lines[1].strip()
                return ssid, password
        except Exception as e:
            print("Error reading credentials:", e)
            return None, None
        
    # connect to wifi with given ssid and password
    def connect_wifi(self, ssid, password):
        import network # pyright: ignore[reportMissingImports]
        import time

        if ssid is None or password is None:
            print("SSID or password is None, cannot connect to WiFi")
            return False

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            print('Connecting to network...')
            wlan.connect(ssid, password)
            timeout = 10  # seconds
            start = time.time()
            while not wlan.isconnected():
                if time.time() - start > timeout:
                    print("Could not connect to WiFi")
                    return False
                time.sleep(1)
        print('Network config:', wlan.ifconfig())
        return True
    

# run the startup sequence if this file is run directly
if __name__ == "__main__":
    micropython.alloc_emergency_exception_buf(100)

    boot_config = BootConfig()
