from picar import front_wheels
from picar import back_wheels
import time
import picar

picar.setup

fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')

def start_bouge():
    
    
    
    fw.turn_straight()
    bw.forward()
    bw.speed = 100
    time.sleep(5)
    
    
    fw.turn(0)
    
    bw.backward()
    bw.speed = 100
    time.sleep(5)
    
    fw.turn(180)
    time.sleep(3)
    fw.turn(90)
    
    bw.stop()
    fw.turn_straight()
    
def stop():
    bw.stop()
    fw.turn_straight()
    
if __name__ == '__main__':
    try:
        start_bouge()
    except KeyboardInterrupt:
        stop()
    
