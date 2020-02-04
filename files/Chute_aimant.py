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
    file = open(file)
    csv_file = csv.reader(file, delimiter = ";")
    for row in csv_file:
        Tableau.append(row)   
    file.close
    n = len(Tableau)
    for i in range(1,n):
        Data.append(float(Tableau[i][k].replace(",", ".")))         
    return Data

def  passe_bas(liste, te, tau):
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

for k in range(0, N): #Tracer les courbes de tension bornes bobine
    name = noms[k].replace('.csv', "")
    temps = convertisseur(noms[k], 0)
    bobine1 = passe_bas(convertisseur(noms[k], 1), te, tau)
    bobine2 = passe_bas(convertisseur(noms[k], 3), te, tau)
    plt.plot(temps, bobine1, label="$Bobine\:1$")
    plt.plot(temps, bobine2, label="$Bobine\:2$")
    plt.legend(loc='upper right')
    plt.xlabel('$Temps\:(s)$', fontsize=16)
    plt.ylabel('$Tension\:(V)$', fontsize=16)
    plt.title("$Chute\:d'un\:aimant\:dans\:un\:tube\:en\:cuivre$", fontsize=20)
    plt.grid()
#    plt.savefig('chute_cuivre.png')
    plt.show()

Tcu, Vcu = [], [] #Calcul de la vitesse dans le tube en cuivre
for k in range(0, 9):
    temps = convertisseur(noms[k], 0)
    tension_bobine1 = passe_bas(convertisseur(noms[k], 1), te, tau)
    tension_bobine2 = passe_bas(convertisseur(noms[k], 3), te, tau)
    T1, T2 = pic(tension_bobine1, temps), pic(tension_bobine2, temps)
    distance = float(noms[k][11:13])*10**(-3)
    vitesse = distance/(abs(T2[-2]-T1[-2]))
    Tcu.append(distance), Vcu.append(vitesse)
#    print(vitesse)

Tpvc, Vpvc = [], [] #Calcul de la vitesse dans le tube en PVC
for k in range(9, N): 
    temps = convertisseur(noms[k], 0)
    bobine1 = passe_bas(convertisseur(noms[k], 1), te, tau)
    bobine2 = passe_bas(convertisseur(noms[k], 3), te, tau)
    T1, T2 = pic(bobine1, temps), pic(bobine2, temps)
    distance = float(noms[k][11:13])*10**(-3)
    vitesse = distance/(T2[-2]-T1[-2])
    Tpvc.append(distance), Vpvc.append(vitesse)
#    print(vitesse)


Modelcu = np.polyfit(Tcu, Vcu, 1) #Permet de modéliser vitesse cuivre
def Vmodelcu(x):
    return (float(Modelcu[1]) + float(Modelcu[0])*x) 
VmodCu = [(Vmodelcu(t)) for t in Tcu]
        
Modelpvc = np.polyfit(Tpvc, Vpvc, 1) #Permet de modéliser vitesse PVC
def Vmodelpvc(x):
    return float(Modelpvc[1]) + float(Modelpvc[0])*x 
Vmodpvc = [Vmodelpvc(d) for d in Tpvc]
          
plt.plot(Tcu, Vcu, '+b', label="$Cuivre$")
plt.plot(Tpvc, Vpvc, '+g', label="$PVC$")
plt.plot(Tcu, VmodCu, '-b', label="$v="+ "%.1f" % Modelcu[1]+ "$+$" "%.2f" \
         % Modelcu[0] + "*d %$")
plt.plot(Tpvc, Vmodpvc,'-g', label="$v="+ "%.1f" % Modelpvc[1]+ "$+$" "%.2f" \
         % Modelpvc[0] + "*t %$")
plt.legend(loc='best', prop={'size': 15})
plt.title(r"$Vitesse\:moyenne\:en\:fonction\:de\:la\:distance$",  fontsize=17)
plt.xlabel(r'$Distance \:(m)$', fontsize=16)
plt.ylabel(r'$Vitesse\:(m/s)$', fontsize=16)
plt.grid()
plt.show()

#
