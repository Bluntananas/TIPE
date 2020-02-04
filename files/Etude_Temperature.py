# -*- coding: utf-8 -*-
"""
@author: Antho
"""
import glob as gb
import csv
import matplotlib.pyplot as plt
import numpy as np

def convertisseur(file, k):
    Tableau = []
    Data = []
    f = open(file)
    csv_f = csv.reader(f, delimiter = ";")
    for row in csv_f:
        Tableau.append(row)   
    f.close
    n = len(Tableau)
    for i in range(1,n):
        Data.append(float(Tableau[i][k].replace(",", ".")))         
    return Data

def  passe_bas(liste,te,tau):
    liste_filtre=[liste[0]]
    n = len(liste)
    for k in range(n-1):
        liste_filtre.append(liste_filtre[k]+te/tau*(liste[k]-liste_filtre[k]))
    return liste_filtre

def pic(tension, temps):
    n = len(tension)
    pics = []
    for k in range(10,n):
        if abs(tension[k-10]) > 0.02:
                if tension[k-1] > 0 and tension[k+1] < 0 or \
                tension[k-1] < 0 and tension[k+1] > 0 :
                    pics.append(temps[k])
    return pics

te = 1E-4
tau = 0.0005

noms= gb.glob("*.csv")
N = len(noms)

Temperature = [ 29, 40, 55, 70, 75]
Vitesse = []

for k in range(0, N): #calcul de la vitesse 
    name = noms[k].replace('.csv', "")
    temps = convertisseur(noms[k], 0)
    bobine1 = passe_bas(convertisseur(noms[k], 1), te, tau)
    bobine2 = passe_bas(convertisseur(noms[k], 3), te, tau)
    T1, T2 = pic(bobine1, temps), pic(bobine2, temps)
    distance = 55*10**(-3)
    v = distance/(abs(T1[0]-T2[0]))
    Vitesse.append(v)
#    print(v)

Model = np.polyfit(Temperature, Vitesse, 1)
def Vmodel(x):
    return float(Model[1]) + float(Model[0])*x 
Vitesse_mod = [Vmodel(T) for T in Temperature]
        
plt.plot(Temperature, Vitesse, '+', label="$Points\:expérimentaux$")
plt.plot(Temperature, Vitesse_mod, '-', label="$Modèle\::\:v="+ "%.1f" % \
         Model[1]+ "$+$" "%.2f" % Model[0] + "*T %$")
plt.grid()
plt.legend(loc='best')
plt.title(r"$Variation\:de\:la\:vitesse\:en\:fonction\:de\:la\:température$" \
          ,fontsize=17)
plt.xlabel(r'$Temperature \:(^{\circ} C)$', fontsize=16)
plt.ylabel(r'$Vitesse\:(m/s)$', fontsize=16)
plt.show()

    
