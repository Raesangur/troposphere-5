import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
from scipy import interpolate

rayon = 20
h = np.arange(-rayon, rayon, 1/10000)
masse_bille = 0.005
g = 9.81

# depth = 1.5 mm
# size = 40 mm
hauteur_coupole = 0.00375 * h ** 2

acceleration = np.arange(-rayon, rayon, 1/10000)
# vitesse = np.gradient(acceleration)


def energie_potentielle(masse, hauteur):
    return g * masse * hauteur

# def energie_cinetique(masse,vitesse):
#     return 1/2 * masse * (vitesse ** 2)


def inertie(masse, accel):
    return masse * accel


# def hauteur_calculator():
x = np.arange(0, 20+1/1000, 1/1000)
x1 = np.arange(0, 100+1, 1)
hauteur = 0.00375 * x ** 2

vitesse = np.sqrt((2 * ((inertie(masse_bille, 0.736) * x) -
                  energie_potentielle(masse_bille, hauteur))) / masse_bille)
plt.rcParams["figure.figsize"] = (15, 4)
plt.plot(x, vitesse)
plt.title(
    "Vitesse en fonction de la position en x avec une accélération de 0.736 m/s²")
plt.ylabel("Vitesse en m/s")
plt.xlabel("Position en x(mm)")
plt.show()
v= interpolate.PchipInterpolator(x,vitesse)
vt= interpolate.UnivariateSpline(x,vitesse)
plt.rcParams["figure.figsize"] = (15, 4)
acc = vt.derivative() # dérivée n-ième

plt.plot(acc(x1))
plt.title(
    "accélération en fonction de la position en x avec une accélération de la voiture de 0.736 m/s²")
plt.ylabel("accélération en m/s²")
plt.xlabel("Position en x(mm)")
plt.show()
plt.rcParams["figure.figsize"] = (15, 4)
plt.plot(h, hauteur_coupole)
plt.title("Coupole")
plt.ylabel("Hauteur en mm")

# freshly stolen from https://stackoverflow.com/questions/332289/how-do-i-change-the-size-of-figures-drawn-with-matplotlib
plt.rcParams["figure.figsize"] = (15, 4)
plt.plot(0, 0.05, marker="o", markersize=10,
         markeredgecolor="green", markerfacecolor="green")
plt.show()


temps = np.arange(0, 60*1/200, 1/500)
# pos = 1/2 * y_n(0)  * temps[1] ** 2 = 8.005265733132975e-07
pos = []
descente = False
for i in range(len(temps)):
    if i == 0:
        pos.append(0)
    else:
        if pos[i-1] > 19.9 and descente == False and v(pos[i-1]) > 0:
            descente = True
        if pos[i-1] < 1 and v(pos[i-1]) < 0:
            descente = False
        if descente == False:
            pos.append((pos[i-1]) + (v(pos[i-1]) * temps[i]) + (1/2 * acc(pos[i-1])  * (temps[i] ** 2)))
        else:
            pos.append((pos[i-1]) - (v(pos[i-1]) * temps[i]) + (1/2 * acc(pos[i-1])  * (temps[i] ** 2)))

# create the figure and axes objects
fig, ax = plt.subplots()
# create the animation function
def animateboule(i):
    x = pos[i]
    y = 0.00375 * x ** 2 + 0.05
    ax.clear()
    ax.plot(h, hauteur_coupole)
    ax.set_title(
        "Position en fonction du temps avec une accélération de 0.736 m/s²")
    ax.set_ylabel("Hauteur en mm")
    ax.set_xlabel("Position en mm")
    fig.set_figheight(4)
    fig.set_figwidth(15)
    ax.plot(x, y, marker="o", markersize=10,
            markeredgecolor="green", markerfacecolor="green")


ani = FuncAnimation(fig, animateboule, frames=len(pos), interval=50)
f = r"D:/Documents/uni/S5/projet/pos_coupole.gif"
ani.save(f,writer=PillowWriter(fps=15))
plt.show()
