from SunFounder_Ultrasonic_Avoidance import Ultrasonic_Avoidance
import csv
import time

UA = Ultrasonic_Avoidance.Ultrasonic_Avoidance(20)


def main():
    N = 100
    with open('distance.csv', 'w') as f:    
        writer = csv.writer(f)
        for i in range(N):
	        distance = UA.get_distance()
	        if distance != -1:
		        print(distance)
		        time.sleep(0.2)
		        writer.writerow([str(distance)])
	        else:
		        print(False)
        
if __name__=='__main__':
	main()
