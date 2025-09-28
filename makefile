# automation for putting files using ampy in port COM5
PORT = COM5
FILES = main.py boot.py
LIBS = mpu6500.py ak8963.py mpu9250.py
AMPY = ampy -p $(PORT)
PYTHON = python

.PHONY: all 

all: put sync_lib sync_secret

get_data:
	$(AMPY) get imu_data.txt ampy_get/imu_data/imu_data.txt
# put them separately to avoid ampy timeout issues
put:
	$(AMPY) put boot.py
	$(AMPY) put main.py

sync_lib:
	$(AMPY) put mpu6500.py
	$(AMPY) put ak8963.py
	$(AMPY) put mpu9250.py

sync_secret:
	$(AMPY) put secret.txt

reset:
	$(AMPY) reset

# in this working directory, theres a ampy_get dir, put the results of get in that
get:
	$(AMPY) get main.py ampy_get/scripts/main.py
	$(AMPY) get boot.py ampy_get/scripts/boot.py
	$(AMPY) get mpu6500.py ampy_get/scripts/mpu6500.py
	$(AMPY) get ak8963.py ampy_get/scripts/ak8963.py
	$(AMPY) get mpu9250.py ampy_get/scripts/mpu9250.py
	$(AMPY) get secret.txt ampy_get/scripts/secret.txt

run:
	$(AMPY) run main.py

