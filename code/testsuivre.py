from picar import front_wheels
from picar import back_wheels
from SunFounder_Ultrasonic_Avoidance import Ultrasonic_Avoidance
import picar
import time
import smbus
import math

class Line_Follower(object):
	def __init__(self, address=0x11, references=[10, 10, 10, 10, 10]):
		self.bus = smbus.SMBus(1)
		self.address = address
		self._references = references

	def read_raw(self):
		for i in range(0, 5):
			try:
				raw_result = self.bus.read_i2c_block_data(self.address, 0, 10)
				Connection_OK = True
				break
			except:
				Connection_OK = False

		if Connection_OK:
			return raw_result
		else:
			return False
			print("Error accessing %2X" % self.address)

	def read_analog(self, trys=5):
		for _ in range(trys):
			raw_result = self.read_raw()
			if raw_result:
				analog_result = [0, 0, 0, 0, 0]
				for i in range(0, 5):
					high_byte = raw_result[i*2] << 8
					low_byte = raw_result[i*2+1]
					analog_result[i] = high_byte + low_byte
					if analog_result[i] > 1024:
						continue
				return analog_result
		else:
			raise IOError("Line follower read error. Please check the wiring.")

	def read_digital(self):	
		lt = self.read_analog()
		digital_list = []
		for i in range(0, 5):
			if lt[i] > self._references[i]:
				digital_list.append(False)
			elif lt[i] <= self._references[i]:
				digital_list.append(True)
			else:
				digital_list.append(-1)
		return digital_list

	def get_average(self, mount):
		if not isinstance(mount, int):
			raise ValueError("Mount must be interger")
		average = [0, 0, 0, 0, 0]
		lt_list = [[], [], [], [], []]
		for times in range(0, mount):
			lt = self.read_analog()
			for lt_id in range(0, 5):
				lt_list[lt_id].append(lt[lt_id])
		for lt_id in range(0, 5):
			average[lt_id] = int(math.fsum(lt_list[lt_id])/mount)
		return average

	def found_line_in(self, timeout):
		if isinstance(timeout, int) or isinstance(timeout, float):
			pass
		else:
			raise ValueError("timeout must be interger or float")
		time_start = time.time()
		time_during = 0
		while time_during < timeout:
			lt_status = self.read_digital()
			result = 0
			if 1 in lt_status:
				return lt_status
			time_now = time.time()
			time_during = time_now - time_start
		return False

	def wait_tile_status(self, status):
		while True:
			lt_status = self.read_digital()
			if lt_status in status:
				break

	def wait_tile_center(self):
		while True:
			lt_status = self.read_digital()
			if lt_status[2] == 1:
				break

	@property
	def references(self):
		return self._references
	import picar
	@references.setter
	def references(self, value):
		self._references = value

picar.setup
fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')

def start_bouge():
    UA = Ultrasonic_Avoidance.Ultrasonic_Avoidance(20)
    fw.turn_straight()
    while True:
        distance = UA.get_distance()
        if distance != -1:
            print(distance)
            if distance < 5:
                start_moving(lf = Line_Follower())    
            time.sleep(0.2)
    
def start_moving(lf):
    while lf.read_digital() != [True, True, True, True, True]:
        if lf.read_digital() == [False, False, True, False, False]:
            print("straight")
            fw.turn_straight()
            bw.speed = 70
            bw.backward()
        elif lf.read_digital() == [False, True, True, False, False] or [False, True, False, False, False] :
            print("right")
            fw.turn_left()
            bw.speed = 30
            bw.backward()  
        elif lf.read_digital() == [False, False, True, True, False] or [False, False, False,True, False] :
            print("left")
            fw.turn_rigth()
            bw.speed = 30
            bw.backward() 
    print("Found line")
    stop()
   

def stop():
    bw.stop()
    fw.turn_straight()
    
if __name__ == '__main__':
    try:
        time.sleep(10)
        start_bouge()
    except KeyboardInterrupt:
        stop()