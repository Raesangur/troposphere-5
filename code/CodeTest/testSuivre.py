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
    
def start_moving(lf, vitesseBase = 100):
    lState = ""
    angle = 90
    WTF = False 
    while lf.read_digital() != [True, True, True, True, True]:
        rd = lf.read_digital()
        #print(rd)
        if rd == [False, False, True, False, False] :
            angle = 0
            vitesseBase = 90
        if rd == [False, True, True, False, False] or rd == [False, False, True, True, False]:
            angle = 10
            vitesseBase = 90
        if rd == [False, True, False, False, False] or rd == [False, False, False, True, False]:
            angle = 20
            vitesseBase = 85
        if rd == [True, True, False, False, False] or rd == [False, False, False, True, True]:
            angle = 30
            vitesseBase = 80
        if rd == [True, False, False, False, False] or rd == [False, False, False, False, True] or rd == [True, True, True, False, False] or rd == [False, False, True, True, True]:
            angle = 45
            vitesseBase = 75

        if rd == [False, False, True, False, False]:
            angle = 90
        elif rd == [False, False, True, True, False] or rd == [False, False, False, True, False] or rd == [False, False, False, True, True] or rd == [False, False, False, False, True] or rd == [False, False, True, True, True]:
            angle = 90 + angle
        elif rd == [False, True, True, False, False] or rd == [False, True, False, False, False] or rd == [True, True, False, False, False] or rd == [True, False, False, False, False] or rd == [True, True, True, False, False]:
            angle = 90 - angle
        else:
            WTF = True
            print("Continue")
            
        if WTF == True :
            fw.turn(-angle)
            bw.speed = (65*0.4)
            bw.forward()
            time.sleep(0.5)
            WTF = False
        else :        
            fw.turn(angle)
            bw.speed = int(vitesseBase * 0.8)
            bw.backward()
            time.sleep(0.01)

        
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
