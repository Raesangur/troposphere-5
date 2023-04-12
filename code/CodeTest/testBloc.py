from picar import front_wheels
from picar import back_wheels
import time
import picar

picar.setup

fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')

def start_bouge():

    
    fw.turn_straight()
    bw.backward()
    bw.speed = 85
    time.sleep(3)
    fw.turn(45)
    time.sleep(4)
    fw.turn_straight()
    time.sleep(3)
    stop()

#    fw.turn_straight()
 
def stop():
    bw.stop()
    fw.turn_straight()
    
if __name__ == '__main__':
    try:
        time.sleep(15)
        start_bouge()
    except KeyboardInterrupt:
        stop()
    
