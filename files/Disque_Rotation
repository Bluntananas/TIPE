# -*- coding: utf-8 -*-
"""
@author: Antho
"""
import glob as gb
import csv
import matplotlib.pyplot as plt
import numpy as np
from lmfit import Model
 
def convertisseur(file, k):
    Tableau = []
    Temps = []
    f = open(file)
    csv_f = csv.reader(f, delimiter = ";")
    for row in csv_f:
        Tableau.append(row)   
    f.close
    n = len(Tableau)
    for i in range(1,n):
        Temps.append(float(Tableau[i][k].replace(",", ".")))         
    return Temps
     
def detection_pic(liste, seuil):
    n = len(liste)
    pics = []
    for k in range(n-1):
        if liste[k] < seuil and liste[k+1] >= seuil:
            pics.append(k)
    return pics
     
def vitesse(pics, temps):
    angle = np.pi/6
    n = len(pics)
    omega = []
    T = []
    for k in range(n-1):       
        t1 = pics[k+1]
        t0 = pics[k]
        omega.append(angle/(temps[t1]-temps[t0]))   
        T.append(temps[int((t0+t1)/2)])        
    return np.array(omega, dtype=float), np.array(T, dtype=float)

def expo(x, tau, alpha):
    return (T[0]+alpha/Fs)*np.exp(-x/tau) - alpha/Fs 
  
    
noms= gb.glob("*.csv")
Fs = -2.37626e-10 #Couple frottement solide
Js = (0.5)*0.400*(6e-3)**2 #Moment d'inertie du disque
gmodel, N = Model(expo), len(noms)

######Permet de calculer/tracer TAU et ALPHA en fonction de I ###### 

Tau = [] 
alpha = []
I =[]
for k in range(2, N):
    name = noms[k].replace('.csv', "")
    temps = convertisseur(noms[k], 0)
    tension = convertisseur(noms[k], 1)
    pics = detection_pic(tension, 2.5)
    T, V = vitesse(pics, temps)
    resultbis = gmodel.fit(T, x=V, tau = 10, alpha = 1)
    tau = "%.2f" % resultbis.values['tau']
    Tau.append(tau)
    a = resultbis.values['alpha']
    alpha.append(a)
    i = name[2] + '.' + name[3:5]
    I.append(i)

fig, ax1 = plt.subplots()

color = 'r'
ax1.set_xlabel('$Intensité\:(A)$', fontsize=17)
ax1.set_ylabel(r"$\tau$", fontsize=19, color=color)
ax1.plot(I, Tau, '+:', color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax2 = ax1.twinx()  
color = 'b'
ax2.set_ylabel(r"$\alpha$", fontsize=19, color=color) 
ax2.plot(I, alpha, '+:', color=color)
ax2.tick_params(axis='y', labelcolor=color)
fig.tight_layout()  
plt.grid()
plt.title(r"$Variation\:de\:\tau\:et\:\alpha\:en\:fonction\:de\:l'intensité$"\
          , fontsize = 18)
plt.show()

######Permet de tracer Vreel et Vmodelisation pour chaque I ###### 

for k in range(2, N): 
    name = noms[k].replace('.csv', "")
    temps = convertisseur(noms[k], 0)
    tension = convertisseur(noms[k], 1)
    pics = detection_pic(tension, 2.5)
    T, V = vitesse(pics, temps)
    resultbis = gmodel.fit(T, x=V, tau = 10, alpha = 1)
    print(resultbis.fit_report())
    tau = "%.2f" % resultbis.values['tau']
    plt.plot(V, T, 'b', label="$Data$")
    plt.plot(V, resultbis.best_fit, 'r-', label='$Model : tau='+tau+'s$')    
    plt.title('I=' + name[2] + '.' + name[3:5] + ' A') 
    plt.title("$Tension\:aux\:bornes\:de\:la\:photodiode$",  fontsize=18)
    plt.legend(loc='upper right')
    plt.plot(temps, tension)
    plt.ylabel("$Tension\:(V)$",  fontsize=17)
    plt.xlabel("$Temps\:(s)$",  fontsize=17)
    plt.grid()
    plt.show()
    plt.savefig('I=' + name[2] + '.' + name[3:5] + ' A.png')
    plt.close()

 
######Permet de calcuer et d'afficher 1/TAU=f(i**2) ###### 
    
Tau = [] 
Taubis = []
I, I2 = [], []
for k in range(1, N-2):
    name = noms[k].replace('.csv', "")
    temps = convertisseur(noms[k], 0)
    tension = convertisseur(noms[k], 1)
    pics = detection_pic(tension, 2.5)
    T, V = vitesse(pics, temps)
    resultbis = gmodel.fit(T, x=V, tau = 10, alpha = 1)
    tau = "%.2f" % resultbis.values['tau']
    taubis = 1/float(tau)
    Taubis.append(taubis)
    Tau.append(tau)
    i = float(name[2] + '.' + name[3:5])
    I2.append(i**2)
    I.append(i)

Model = np.polyfit(I2, Taubis, 1)
#print(a, b)    

def tauMod(x):
    return 0.015 + Model[0]*x
TauM = []    
for k in range(len(I2)):
    TauM.append(tauMod(I2[k]))

plt.plot(I2, Taubis, 'b+')
plt.plot(I2, TauM, 'b--', label="$Modele\::"+"%.3f" % Model[1]+ "$+$" "%.2f" \
         % Model[0]+".i^2$")
plt.xlabel(r'$Intensité \:(A)$', fontsize=16)
plt.legend(loc='best')
plt.ylabel(r'$\frac{1}{\tau}\:(s^{-1})$', fontsize=16)
plt.title(r'$Variation \:de \: \frac{1}{\tau} \:en \:fonction \:de \:i^{2}$' \
          ,  fontsize=17)
plt.grid()
plt.plot()
plt.show()
