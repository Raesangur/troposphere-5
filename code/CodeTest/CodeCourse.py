from picar import front_wheels
from picar import back_wheels
from SunFounder_Ultrasonic_Avoidance import Ultrasonic_Avoidance
from LineFollower import Line_Follower
import picar
import time
import smbus
import math
import sys, getopt
picar.setup()
fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')
facteurVitesse = 0.5
vitesseErreur = 25
straightMax = 110
delay = 0.01
delayError = 0.45
errorThreshold = 110
errorMax = 150
lineCalibration = 17
obstacleDistance = 14
distanceDutyCycle = 10

def start_bouge():
    UA = Ultrasonic_Avoidance.Ultrasonic_Avoidance(20)
    fw.turn_straight()
    while True:
        distance = UA.get_distance()
        if distance < 20:
            time.sleep(0.2)
            start_moving(Line_Follower(references=[lineCalibration, lineCalibration, lineCalibration, lineCalibration, lineCalibration]), UA)    
    
def start_moving(lf,UA, vitesseBase = 100):
    angle = 90
    erreur = 0
    straight = 0
    vitesseBase = 100
    cpt = 0
    rd = lf.read_digital()
    
    while rd != [True, True, True, True, True]:
        rd = lf.read_digital()

        if rd == [False, False, True, False, False] :
            angle = 0
            vitesseBase = 90 + straight / 10
            if straight < straightMax:
                straight += 1
        if rd == [False, True, True, False, False] or rd == [False, False, True, True, False]:
            angle = 12
            vitesseBase = 80 + straight / 10
            if straight > 0:
                straight -= 1
        if rd == [False, True, False, False, False] or rd == [False, False, False, True, False]:
            angle = 24
            vitesseBase = 75 + straight / 10
            if straight > 0:
                straight -= 1
        if rd == [True, True, False, False, False] or rd == [False, False, False, True, True]:
            angle = 35
            vitesseBase = 70 + straight / 10
            if straight > 0:
                straight -= 1
        if rd == [True, False, False, False, False] or rd == [False, False, False, False, True] or rd == [True, True, True, False, False] or rd == [False, False, True, True, True]:
            angle = 45
            vitesseBase = 65 + straight / 10
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
            
        if erreur >= errorThreshold and  angle != 90:
            fw.turn(180 - angle)
            bw.speed = int(vitesseErreur + (erreur*5 / (errorThreshold)))
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
            cpt += 1
            #erreur = 0

        
        if (angle > 85 and angle < 95) and 0 == cpt%distanceDutyCycle:
            distance = UA.get_distance()
            distance += UA.get_distance()
            distance /= 2
            if distance <= obstacleDistance:
                bw.stop()
                obstacle_avoidance(lf,UA)
            cpt = 0    
        
    
    stop()
   
def stop():
    bw.stop()
    fw.turn_straight()
    

def obstacle_avoidance(lf,UA):
    vit = 40
    bw.stop()

    # On est a la ligne de 10cm 
    time.sleep(3)
    bw.speed = vit
    fw.turn_straight()
    bw.forward()
    time.sleep(2.6)
    
    bw.stop()
    distance = UA.get_distance()
    while (distance <28):
        bw.speed = vit
        bw.forward()
        distance = UA.get_distance()
        time.sleep(0.01)
    bw.stop()
    fw.turn(45)
    time.sleep(1)
    
    bw.speed = vit
    bw.backward()
    time.sleep(1.5)
    
    bw.stop()
    fw.turn_straight()
    bw.speed = vit
    bw.backward()
    time.sleep(4.3)
    
    bw.stop()
    fw.turn(130)
    bw.speed = vit
    bw.backward()
    

    rd = lf.read_digital()
    while(rd != [False, True, True, False, False] and rd != [True, True, False, False, False] and rd != [False, False, True, True, False] and rd != [False, False, False, True, True]):
        time.sleep(0.01)
        rd = lf.read_digital()
        
    


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
    global distanceDutyCycle
    
    opts, args = getopt.getopt(argv, "hv:s:", ["speed=", "error-speed", "straight=", "delay=", "error-delay=", "line-calibration=", "distance=", "errors=", "errors-max=","distance-duty-cycle="])
    for opt, arg in opts:
        if opt == "-h":
            print("\tTroposphere-5: Projet S5 Genie Informatique 66")
            print("\tVoiture SunFounder Picar\n")
            print("\tusage: troposphere-5.py [-h] [--speed <flt>] [--error-speed <uint>] [--straight <uint>] [--delay <flt>] [--error-delay <flt>] [--line-calibration <int>] [--distance <int>] [--errors <uint>] [--errors-max <uint>]\n")
            print("\toptional arguments:\n")
            print("\t\t-h\t\t\t\t affiche ce message et quitte l'application")
            print("\t\t--speed\t\t <float> facteur multiplicateur de la vitesse [0 - 1] (default = " + str(facteurVitesse) + ")")
            print("\t\t--error-speed\t\t <int> vitesse de reculon en cas de perte de ligne [0 - 100] (default = " + str(vitesseErreur) + ")")
            print("\t\t--straight\t <int> compteur maximal pour l'acceleration en ligne droite (default = " + str(straightMax) + ")")
            print("\t\t--delay\t\t <float> delay en secondes entre les mesures de capteurs [0.001 - 1] (default = " + str(delay) + ")")
            print("\t\t--error-delay\t <float> delay en secondes dans le cas d'une perte de ligne [0.001 - 1] (default = " + str(delayError) + ")")
            print("\t\t--line-calibration\t <int> valeur threshold du suiveur de ligne [0 - 255] (default = " + str(lineCalibration) + ")")
            print("\t\t--distance\t\t <int> distance en cm entre la voiture et l'obstacle avant de commencer la manoeuvre d'evitement [0 - 50] (default = " + str(obstacleDistance) + ")")
            print("\t\t--errors\t\t <int> valeur du compteur d'erreur pour commencer a reculer [0 - 1000] (default = " + str(errorThreshold) + ")")
            print("\t\t--errors-max\t <int> valeur maximale du compteur d'erreur [0 - 1000] (default = " + str(errorMax) + ")")
            print("\t\t--distance-duty-cycle\t <int> Pourcentage de cycle regardant pour un obstacle [0 - 100] (default = " + str(distanceDutyCycle) + ")")
                        
            exit()

        elif opt in ("--speed"):
            fv = float(arg)
            if fv > 0 and fv <= 1:
                facteurVitesse = fv
            elif fv < 0:
                facteurVitesse = 0
            elif fv > 1:
                facteurVitesse = 1
            print("Facteur multiplicateur de la vitesse: " + str(facteurVitesse))

        elif opt in ("--error-speed"):
            v = float(arg)
            if v > 0 and v <= 100:
                vitesseErreur = v
            elif v < 0:
                vitesseErreur = 0
            elif v > 100:
                vitesseErreur = 1
            print("Vitesse en cas de perte de ligne: " + str(vitesseErreur))
            
        elif opt in ("--straight"):
            sm = int(arg)
            if sm > 0:
                straightMax = sm
                print("Compteur maximal d'acceleration en ligne droite: " + str(straightMax))
                
        elif opt in ("--delay"):
            d = float(arg)
            if d >= 0.001 and d <= 1:
                delay = d
            elif d < 0.001:
                delay = 0.001
            elif d > 1:
                delay = 1
            print("Delai entre les mesures de capteurs (s): " + str(delay))

        elif opt in ("--error-delay"):
            d = float(arg)
            if d >= 0.001 and d <= 1:
                delayError = d
            elif d < 0.001:
                delayError = 0.001
            elif d > 1:
                delayError = 1

            print("Delai dans le cas d'une perte de ligne (s): " + str(delayError))

        elif opt in ("--line-calibration"):
            c = int(arg)
            if c > 0 and c <= 255:
                lineCalibration = c
            elif c < 0:
                lineCalibration = 0
            elif c > 255:
                lineCalibration = 255
            print("Threshold du suiveur de ligne: " + str(lineCalibration))

        elif opt in ("--distance"):
            d = int(arg)
            if d > 0 and d <= 50:
                obstacleDistance = d
            elif d < 0:
                obstacleDistance = 0
            elif d > 50:
                obstacleDistance = 50
            print("Threshold du suiveur de ligne: " + str(obstacleDistance))

        elif opt in ("--errors"):
            e = int(arg)
            if e > 0 and e <= 1000:
                errorThreshold = e
            elif e < 0:
                errorThreshold = 0
            elif e > 1000:
                errorThreshold = 1000
            print("Nombre d'erreurs avant de commencer a reculer: " + str(errorThreshold))

        elif opt in ("--errors-max"):
            e = int(arg)
            if e > 0 and e <= 1000:
                errorMax = e
            elif e < 0:
                errorMax = 0
            elif e > 1000:
                errorMax = 1000
            print("Nombre d'erreurs maximum: " + str(errorMax))
        elif opt in ("--Distance-duty-cycle"):
            e = int(arg)
            if e > 0 and e <= 100:
                errorMax = e
            elif e < 0:
                errorMax = 0
            elif e > 100:
                errorMax = 100
            print("Distance duty cycle: " + str(errorMax))
            
            
if __name__ == '__main__':
    try:
        get_args(sys.argv[1:])
        
        time.sleep(10)
        start_bouge()
    except KeyboardInterrupt:
        stop()
