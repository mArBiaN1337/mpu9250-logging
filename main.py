from mpu9250 import MPU9250
from boot import BootConfig
from machine import I2C, Pin 
import utime 
#pyright: reportMissingImports=false

class IMUDataLogger:
    def __init__(self):
        
        #setup imu
        i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
        self.mpu = MPU9250(i2c)
        self.led = BootConfig.DATA_LED

        self.write_log_headers()

        self.log_data()

    def write_log_headers(self):
        with open("imu_data.txt", "w") as f:
            # fix indentation of headers with units
            # take the space before the headers in the file
            f.write("ax (m/s^2), ay (m/s^2), az (m/s^2), gx (rps), gy (rps), gz (rps), temp (C)\n")
            f.flush()

    def log_data(self, samples=200):
        print("Logging {} samples...".format(samples))
        with open("imu_data.txt", "a") as f:
            # sometimes the file doesnt have the amount of samples 
            # so we log a bit more to be sure
            for _ in range(2*samples):
                self.led.toggle()  # toggle data led to indicate logging
                ax, ay, az = self.mpu.acceleration  # in m/s^2
                gx, gy, gz = self.mpu.gyro          # in rad/s
                #mx, my, mz = self.mpu.magnetic      # in uT
                temp = self.mpu.temperature         # in C

                # write data to file with commas and newline
                f.write("{:.5f}, {:.5f}, {:.5f}, {:.5f}, {:.5f}, {:.5f}, {:.5f}\n".format(ax, ay, az, gx, gy, gz, temp))
                f.flush()  # ensure data is written to file

        print("Logging complete.")        
        
    # use imu_data.txt to build a http server to serve the data
    def setup_data_server(self):
        import socket

        addr = socket.getaddrinfo(BootConfig.get_ip(), 80)
        print("Starting data server at {}".format(addr[0][4]))
        s = socket.socket()
        s.bind(addr[0][4])
        s.listen(1)
        print('Listening on', addr)
        while True:
            cl, addr = s.accept()
            print('Client connected from', addr)
            with open("imu_data.txt", "r") as f:
                data = f.read()
                # fix indentation
                response = "HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\n{}".format(data)

            cl.send(response)

            cl.close()

if __name__ == "__main__":

    data_logger = IMUDataLogger()

    

