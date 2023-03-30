from picar import front_wheels
from picar import back_wheels
from SunFounder_Ultrasonic_Avoidance import Ultrasonic_Avoidance
from LineFollower import Line_Follower
import picar
import time
import smbus
import math

picar.setup()
fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')

    
def start_moving(lf, targetSpeed = 100):
    currentSpeed = 0
    deltaSpeed = 1
    deltaTime = 0.01
    maxSpeed = targetSpeed
    while True:
        print(str(currentSpeed) + " - " + str(targetSpeed))
        fw.turn_straight()

        if currentSpeed >= 0:
            bw.backward()
            bw.speed = int(currentSpeed)
        else:
            bw.forward()
            bw.speed = -int(currentSpeed)

        if currentSpeed < targetSpeed:
            currentSpeed += deltaSpeed
        elif currentSpeed > targetSpeed:
            currentSpeed -= deltaSpeed

        if lf.read_digital() == [True, True, True, True, True]:
            targetSpeed = -100
            
        time.sleep(deltaTime)

        
    print("Found line")
    stop()
   
def stop():
    bw.stop()
    fw.turn_straight()
    
if __name__ == '__main__':
    try:
        start_moving(lf = Line_Follower())
    except KeyboardInterrupt:
        stop()
