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
            vitesseBase = 80
        if rd == [True, True, False, False, False] or rd == [False, False, False, True, True]:
            angle = 30
            vitesseBase = 75
        if rd == [True, False, False, False, False] or rd == [False, False, False, False, True]:
            angle = 45
            vitesseBase = 60

        if rd == [False, False, True, False, False]:
            angle = 90
        elif rd == [False, False, True, True, False] or rd == [False, False, False, True, False] or rd == [False, False, False, True, True] or rd == [False, False, False, False, True]:
            angle = 90 + angle
        elif rd == [False, True, True, False, False] or rd == [False, True, False, False, False] or rd == [True, True, False, False, False] or rd == [True, False, False, False, False]:
            angle = 90 - angle
        else:
            WTF = True
            vitesseBase = 90
            print("wtf")

        if WTF == True:
            bw.forward()
            bw.speed = int(vitesseBase * 0.3)
            time.sleep(0.5)
            WTF = False
        else:
            fw.turn(angle)
            bw.speed = int(vitesseBase * 0.3)
            bw.backward()
            time.sleep(0.01)
        
        continue
        if rd == [False, False, True, False, False]:
            if lState != "S" :
                if lState == "L" or lState == "R":
                    print("conversion therapy")
                    time.sleep(0.5)
                print("straight")
                fw.turn_straight()
                bw.speed = vitesseBase * 0.5
                bw.backward()
                lState ="S"
                time.sleep(0.1)
        elif rd == [False, True, True, False, False] or rd == [False, True, False, False, False] or rd == [True, True, False, False, False] or rd == [True, False, False, False, False] :
            if lState != "L" :
                print("left")
                fw.turn_left()
                bw.speed = vitesseBase * 0.3
                bw.backward()
                lState = "L"
                time.sleep(0.1) 
        elif rd == [False, False, True, True, False] or rd == [False, False, False,True, False] or rd == [False, False, False, True, True] or rd == [False, False, False, False, True]:
            if lState != "R" :
                print("right")
                fw.turn_right()
                bw.speed = int(vitesseBase * 0.3)
                bw.backward()
                lState = "R"
                time.sleep(0.1)
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
