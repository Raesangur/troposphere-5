import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter

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
hauteur = 0.00375 * x ** 2
vitesse = np.sqrt((2 * ((inertie(masse_bille, 0.736) * x) - energie_potentielle(masse_bille, hauteur))) / masse_bille)
plt.rcParams["figure.figsize"] = (15, 4)
plt.plot(x, vitesse)
plt.title("Vitesse en fonction de la position en x avec une accélération de 0.736 m/s²")
plt.ylabel("Vitesse en m/s")
plt.xlabel("Position en x(mm)")
plt.show()
plt.plot(h, hauteur_coupole)
plt.title("Coupole")
plt.ylabel("Hauteur en mm")

# freshly stolen from https://stackoverflow.com/questions/332289/how-do-i-change-the-size-of-figures-drawn-with-matplotlib
plt.rcParams["figure.figsize"] = (15, 4)
plt.plot(0, 0.05, marker="o", markersize=10,
         markeredgecolor="green", markerfacecolor="green")
plt.show()


temps = np.arange(0, 118*1/500, 1/500)
pos = 1/2 *  0.736 * temps ** 2
# create the figure and axes objects
fig, ax = plt.subplots()

#ax.plot(0, 0.05,marker="o", markersize=10,markeredgecolor="green", markerfacecolor="green")
def animateboule(i):
    x = pos[i]*1000
    y = 0.00375 * x ** 2 + 0.05
    ax.clear()
    ax.plot(h, hauteur_coupole)
    ax.set_title("Position en fonction du temps avec une accélération de 0.736 m/s²")
    ax.set_ylabel("Hauteur en mm")
    ax.set_xlabel("Position en mm")
    fig.set_figheight(4)
    fig.set_figwidth(15)
    ax.plot(x, y,marker="o", markersize=10,markeredgecolor="green", markerfacecolor="green")
    
ani = FuncAnimation(fig, animateboule, frames=len(pos),interval=50)
f = r"D:/Documents/uni/S5/projet/pos_coupole.gif" 
ani.save(f,writer=PillowWriter(fps=15))
plt.show()