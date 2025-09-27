import utime
from machine import Pin 
import micropython
#pyright: reportMissingImports=false

class BootConfig:
    # make the code below but in OOP form
    # pin numbers for the leds
    LED_YELLOW = 4
    LED_BLUE = 23

    # pin number for the data logging button and data led
    DATA_LOGGING_PIN = 34
    DATA_LED = 2
    
    DATA_LED = Pin(DATA_LED, Pin.OUT)

    def __init__(self):
        self.leds = {
            "yellow": Pin(self.LED_YELLOW, Pin.OUT),
            "blue": Pin(self.LED_BLUE, Pin.OUT),
        }
        self.DATA_LED.value(0)  # turn off data led

        ssid, password = self.get_credentials()
        conn_status = self.connect_wifi(ssid, password)
        assert conn_status, "Failed to connect to WiFi"

        utime.sleep(5)  # wait a bit before starting server
        self.DATA_LED.value(1)  # turn on data led to indicate ready to log

    @staticmethod
    def get_ip():
        import network # pyright: ignore[reportMissingImports]
        wlan = network.WLAN(network.STA_IF)
        if wlan.isconnected():
            return wlan.ifconfig()[0]
        else:
            return None

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
        import network
        # pyright: ignore[reportMissingImports]
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        if not wlan.isconnected():
            print(f'Connecting to network...', ssid)
            wlan.connect(ssid, password)

            timeout = 10  # seconds
            start = utime.time()
            while not wlan.isconnected():
                if utime.time() - start > timeout:
                    print("Failed to connect to WiFi")
                    return False
                utime.sleep(1)

        # Esta linha é opcional, mas útil para confirmar o IP após a conexão
        print('Network config:', wlan.ifconfig())
        return True


# run the startup sequence if this file is run directly
if __name__ == "__main__":
    micropython.alloc_emergency_exception_buf(100)

    boot_config = BootConfig()
