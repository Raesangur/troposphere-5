from picar import front_wheels
from picar import back_wheels
from SunFounder_Ultrasonic_Avoidance import Ultrasonic_Avoidance
from LineFollower import Line_Follower
import picar
import time
import smbus
import math

facteurVitesse = 0.55
vitesseErreur = 55
straightMax = 100
delay = 0.01
delayError = 0.3
errorThreshold = 50
errorMax = 75
lineCalibration = 17
obstacleDistance = 10


def start_bouge():
    UA = Ultrasonic_Avoidance.Ultrasonic_Avoidance(20)
    fw.turn_straight()
    while True:
        distance = UA.get_distance()
        if distance != -1:
            print(distance)
            if distance < 5:
                start_moving(lf = Line_Follower(references=[lineCalibration, lineCalibration, lineCalibration, lineCalibration, lineCalibration]))    
            time.sleep(0.2)
    
def start_moving(lf):
    lState = ""
    angle = 90
    erreur = 0
    straight = 0
    vitesseBase = 100
    
    while lf.read_digital() != [True, True, True, True, True]:
        rd = lf.read_digital()

        if rd == [False, False, True, False, False] :
            angle = 0
            vitesseBase = 90 + straight / 10
            if straight < straightMax:
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
            
        if erreur >= errorThreshold and  angle != 90:
            fw.turn(180 - angle)
            bw.speed = int(vitesseErreur * erreur / 100)
            bw.forward()
            time.sleep(delayError)
            if erreur > errorMax:
                erreur = errorMax
            # erreur = 0
        else :        
            fw.turn(angle)
            bw.speed = int(vitesseBase * facteurVitesse)
            bw.backward()
            time.sleep(delay)
            #erreur = 0
        if distance != -1 and angle==90 :
            print(distance)
            if distance < obstacleDistance:
                obstacle_avoidance()    
            else:    
                print("Erreur de lecture du capteur")
        
    print("Found line")
    stop()
   
def stop():
    bw.stop()
    fw.turn_straight()
    
def obstacle_avoidance():
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
    
    while(rd != [False, True, True, False, False] or rd != [True, True, False, False, False]) :
        rd = lf.read_digital()
        time.sleep(delay)


def get_args(argv):
    global facteurVitesse
    global vitesseErreur
    global straightMax
    global delay
    global delayError
    global lineCalibration
    global obstacleDistance
    global errorThreshold
    global errorMax

    opts, args = getopt.getopt(argv, "hv:s:", ["speed=", "error-speed", "straight=", "delay=", "error-delay=", "line-calibration=", "distance=", "errors=", "errors-max="])
    for opt, arg in opts:
        if opt == "-h":
            print("\tTroposphere-5: Projet S5 Genie Informatique 66")
            print("\tVoiture SunFounder Picar\n")
            print("\tusage: troposphere-5.py [-h] [--speed <flt>] [--error-speed <uint>] [--straight <uint>] [--delay <flt>] [--error-delay <flt>] [--line-calibration <int>] [--distance <int>] [--errors <uint>] [--errors-max <uint>]\n")
            print("\toptional arguments:\n")
            print("\t\t-h\t\t\t\t affiche ce message et quitte l'application")
            print("\t\t--speed\t\t <float> facteur multiplicateur de la vitesse [0 - 1] (default = " + facteurVitesse + ")")
            print("\t\t--error-speed\t\t <int> vitesse de reculon en cas de perte de ligne [0 - 100] (default = " + vitesseErreur + ")")
            print("\t\t--straight\t <int> compteur maximal pour l'acceleration en ligne droite (default = " + straightMax + ")")
            print("\t\t--delay\t\t <float> delay en secondes entre les mesures de capteurs [0.001 - 1] (default = " + delay + ")")
            print("\t\t--error-delay\t <float> delay en secondes dans le cas d'une perte de ligne [0.001 - 1] (default = " + delayError + ")")
            print("\t\t--line-calibration\t <int> valeur threshold du suiveur de ligne [0 - 255] (default = " + lineCalibration + ")")
            print("\t\t--distance\t\t <int> distance en cm entre la voiture et l'obstacle avant de commencer la manoeuvre d'evitement [0 - 50] (default = " + obstacleDistance + ")")
            print("\t\t--errors\t\t <int> valeur du compteur d'erreur pour commencer a reculer [0 - 1000] (default = " + errorThreshold + ")")
            print("\t\t--errors-max\t <int> valeur maximale du compteur d'erreur [0 - 1000] (default = " + errorMax + ")")

            exit()

        elif opt in ("--speed"):
            fv = float(arg)
            if fv > 0 and fv <= 1:
                facteurVitesse = fv
            elif fv < 0:
                facteurVitesse = 0
            elif fv > 1:
                facteurVitesse = 1
            print("Facteur multiplicateur de la vitesse: " + facteurVitesse)

        elif opt in ("--error-speed"):
            v = float(arg)
            if v > 0 and v <= 100:
                vitesseErreur = v
            elif v < 0:
                vitesseErreur = 0
            elif v > 100:
                vitesseErreur = 1
            print("Vitesse en cas de perte de ligne: " + vitesseErreur)
            
        elif opt in ("--straight"):
            sm = int(arg)
            if sm > 0:
                straightMax = sm
                print("Compteur maximal d'acceleration en ligne droite: " + straightMax)
                
        elif opt in ("--delay"):
            d = float(arg)
            if d >= 0.001 and d <= 1:
                delay = d
            elif d < 0.001:
                delay = 0.001
            elif d > 1:
                delay = 1
            print("Delai entre les mesures de capteurs (s): " + delay)

        elif opt in ("--error-delay"):
            d = float(arg)
            if d >= 0.001 and d <= 1:
                delayError = d
            elif d < 0.001:
                delayError = 0.001
            elif d > 1:
                delayError = 1

            print("Delai dans le cas d'une perte de ligne (s): " + delayError)

        elif opt in ("--line-calibration"):
            c = int(arg)
            if c > 0 and c <= 255:
                lineCalibration = c
            elif c < 0:
                lineCalibration = 0
            elif c > 255:
                lineCalibration = 255
            print("Threshold du suiveur de ligne: " + lineCalibration)

        elif opt in ("--distance"):
            d = int(arg)
            if d > 0 and d <= 50:
                obstacleDistance = d
            elif d < 0:
                obstacleDistance = 0
            elif d > 50:
                obstacleDistance = 50
            print("Threshold du suiveur de ligne: " + obstacleDistance)

        elif opt in ("--errors"):
            e = int(arg)
            if e > 0 and e <= 1000:
                errorThreshold = e
            elif e < 0:
                errorThreshold = 0
            elif e > 1000:
                errorThreshold = 1000
            print("Nombre d'erreurs avant de commencer a reculer: " + errorThreshold)

        elif opt in ("--errors-max"):
            e = int(arg)
            if e > 0 and e <= 1000:
                errorMax = e
            elif e < 0:
                errorMax = 0
            elif e > 1000:
                errorMax = 1000
            print("Nombre d'erreurs maximum: " + errorMax)

            
            
if __name__ == '__main__':
    try:
        picar.setup()
        fw = front_wheels.Front_Wheels(db='config')
        bw = back_wheels.Back_Wheels(db='config')
        
        time.sleep(10)
        start_bouge()
    except KeyboardInterrupt:
        stop()
