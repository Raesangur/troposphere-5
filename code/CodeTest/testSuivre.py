from picar import front_wheels
from picar import back_wheels
from SunFounder_Ultrasonic_Avoidance import Ultrasonic_Avoidance
from LineFollower import Line_Follower
import picar
import time
import smbus
import math

facteurVitesse = 0.8

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
    erreur = 0
    straight = 0
    while lf.read_digital() != [True, True, True, True, True]:
        rd = lf.read_digital()
        #print(rd)
        if rd == [False, False, True, False, False] :
            angle = 0
            vitesseBase = 90 + straight / 10
            if straight < 100:
                straight += 1
        if rd == [False, True, True, False, False] or rd == [False, False, True, True, False]:
            angle = 12
            vitesseBase = 80
            if straight > 0:
                straight -= 1
        if rd == [False, True, False, False, False] or rd == [False, False, False, True, False]:
            angle = 24
            vitesseBase = 75
            if straight > 0:
                straight -= 1
        if rd == [True, True, False, False, False] or rd == [False, False, False, True, True]:
            angle = 35
            vitesseBase = 70
            if straight > 0:
                straight -= 1
        if rd == [True, False, False, False, False] or rd == [False, False, False, False, True] or rd == [True, True, True, False, False] or rd == [False, False, True, True, True]:
            angle = 45
            vitesseBase = 65
            if straight > 0:
                straight -= 1

        if rd == [False, False, True, False, False]:
            angle = 90
            erreur = 0
        elif rd == [False, False, True, True, False] or rd == [False, False, False, True, False] or rd == [False, False, False, True, True] or rd == [False, False, False, False, True] or rd == [False, False, True, True, True]:
            angle = 90 + angle
            erreur = 0
        elif rd == [False, True, True, False, False] or rd == [False, True, False, False, False] or rd == [True, True, False, False, False] or rd == [True, False, False, False, False] or rd == [True, True, True, False, False]:
            angle = 90 - angle
            erreur = 0
        else:
            erreur += 1
            if straight > 0:
                straight -= 1
            print(erreur)
            
        if erreur >= 50 and  angle != 90:
            fw.turn(180 - angle)
            bw.speed = int(55 * erreur / 100)
            bw.forward()
            time.sleep(0.333333333)
            if erreur > 75:
                erreur = 75
            # erreur = 0
        else :        
            fw.turn(angle)
            bw.speed = int(vitesseBase * 0.55)
            bw.backward()
            time.sleep(0.01)
            #erreur = 0
        if distance != -1 and angle==90 :
            print(distance)
            if distance < 10:
                Bloc()    
            else:    
                print("Erreur de lecture du capteur")
        
    print("Found line")
    stop()
   
def stop():
    bw.stop()
    fw.turn_straight()

def get_args(argv):
    global facteurVitesse

    opts, args = getopt.getopt(argv, "hv:", "vitesse=")
    for opt, arg in opts:
        if opt == "-h":
            print("\tTroposphere-5: Projet S5 Genie Informatique 66")
            print("\tVoiture SunFounder Picar\n")
            print("\tusage: troposphere-5.py [-h] [-v --vitesse <float 0:1>]\n")
            print("\toptional arguments:\n")
            print("\t\t-h\t\t affiche ce message et quitte l'application")
            print("\t\t-v\t\t <float> facteur multiplicateur de la vitesse [0 - 1] (default = 0.8)")

            exit()
        elif opt in ("-v"):
            facteurVitesse = float(arg)
            print("Facteur multiplicateur de la vitesse: " + facteurVitesse)
    
def Bloc():
    # On est a la ligne de 10cm 
    bw.speed = 75
    time.sleep(3)
    fw.turn_straight()
    bw.backward()
    time.sleep(2)
    bw.speed = 0
    fw.turn(62)
    bw.speed = 75
    time.sleep(0.3)
    bw.speed = 0
    fw.turn_straight()
    bw.speed = 75
    time.sleep(3.4)
    bw.speed = 0
    fw.turn(118)
    bw.speed = 75
    time.sleep(0.3)
    fw.turn_straight()
    bw.speed = 75
    time.sleep(1)
    fw.turn(55)
    rd = lf.read_digital()
    while(rd != [False, True, True, False, False] or rd != [True, True, False, False, False] :
        rd = lf.read_digital()
        time.sleep(0.1)
    
if __name__ == '__main__':
    try:
        picar.setup()
        fw = front_wheels.Front_Wheels(db='config')
        bw = back_wheels.Back_Wheels(db='config')
        
        time.sleep(10)
        start_bouge()
    except KeyboardInterrupt:
        stop()
