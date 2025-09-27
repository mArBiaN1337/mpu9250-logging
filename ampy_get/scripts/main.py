from mpu9250 import MPU9250
from boot import BootConfig
from machine import I2C, Pin 
import utime 
#pyright: reportMissingImports=false

class IMUDataLogger:
    def __init__(self):
        
        #setup imu
        # use pull up resistors for i2c
        i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
        self.mpu = MPU9250(i2c)
        self.led = BootConfig.DATA_LED
        self.log_button = BootConfig.DATA_LOGGING_BUTTON

        # setup callback to toggle data led when button is pressed
        # make sure to call the callback only once per press
        self.log_button.irq(trigger=Pin.IRQ_RISING, handler=self.log_button_callback)

        self.write_log_headers()

        print("MPU9250 whoami: 0x{:02x}".format(self.mpu.whoami))
        print("Press the button to log data...")

    def write_log_headers(self):
        with open("imu_data.txt", "w") as f:
            f.write("ax (m/s^2), ay (m/s^2), az (m/s^2), gx (rps), gy (rps), gz (rps), mx (uT), my (uT), mz (uT), temp (C)\n")
            f.flush()

    # each time the button is pressed, log 200 samples of IMU data
    def log_button_callback(self, samples=200):
        print("Button pressed, logging {} samples...".format(samples))
        with open("imu_data.txt", "a") as f:
            for _ in range(samples):
                self.led.toggle()  # toggle data led to indicate logging
                ax, ay, az = self.mpu.acceleration  # in m/s^2
                gx, gy, gz = self.mpu.gyro          # in rad/s
                mx, my, mz = self.mpu.magnetic      # in uT
                temp = self.mpu.temperature         # in C

                # write data to file with commas and newline
                f.write("{:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}\n".format(ax, ay, az, gx, gy, gz, mx, my, mz, temp))
                f.flush()  # ensure data is written to file
                utime.sleep_ms(100)  # log at ~10Hz

    # use imu_data.txt to build a http server to serve the data
    def setup_data_server(self):
        import socket

        addr = socket.getaddrinfo('0.0.0.0', 80)
        s = socket.socket()
        s.bind(addr[0][4])
        s.listen(1)
        while True:
            cl, addr = s.accept()
            with open("imu_data.txt", "r") as f:
                data = f.read()
                response = """\
                            HTTP/1.0 200 OK
                            Content-Type: text/plain

                            {}
                            """.format(data)
            cl.send(response)
            cl.close()

if __name__ == "__main__":
    data_logger = IMUDataLogger()
    while True:
        utime.sleep(1)

    

