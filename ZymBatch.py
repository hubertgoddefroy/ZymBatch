import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import subprocess
import os
import pandas as pd
import numpy as np
import itertools
import sys
import time
import threading

parametres_interf = ['l', 'h0', 'i0', 'max', 'min', 'n', 'n0', 'Nerosion', 'Pdetection', 'pies', 'pixel', 'Pmask',
                     'size', 'Typemask', 'v0', 'inv', 'MethodCycle', 'Resize', 'Ireject', 'Bratio', 'Bmarge', 'Bmask',
                     'LastCycle', 'Bheight', 'Bwidth', 'drsd', 'brsd']
parametres_stat = ['MinVolume', 'MaxVolume', 'VolumeBinSize', 'MinVolumeFrequency', 'VolumeDefinition', 'MinDiameter',
                   'MaxDiameter', 'DiameterBinSize', 'MinDiameterFrequency', 'DiameterDefinition']

parametres_int = ['l', 'h0', 'i0', 'max', 'min', 'Nerosion', 'pies', 'size', 'Typemask', 'v0', 'MethodCycle', 'Ireject',
                  'MinVolume', 'MaxVolume', 'VolumeBinSize', 'MinVolumeFrequency', 'VolumeDefinition', 'MinDiameter',
                  'MaxDiameter', 'DiameterBinSize', 'MinDiameterFrequency', 'DiameterDefinition']
parametres_float = ['n', 'n0', 'Pdetection', 'Pmask', 'Resize', 'Ireject', 'Bratio', 'Bmarge', 'Bmask', 'LastCycle',
                    'Bheight', 'Bwidth', 'drsd', 'brsd']
parametres_str = ['inv', 'VolumeDefinition', 'DiameterDefinition']

chemin_instal_Zyminterne = r'C:\\Users\\Public\\Zymoptiq\\ZymoSoft_V3.1.1\\bin'

images_reconstruction = 'true'

def Zyminterne(chemin_instal_Zyminterne, chemin_Images_input, chemin_parametres_Interf, chemin_parametres_statistiques,
               chemin_Reconstruction, chemin_Synthese, longueur_onde, images_reconstruction):
    # ouvrir l'environnement Zyminterne
    # commande1 = r'cd ' + chemin_instal_Zyminterne
    # subprocess.run(commande1, capture_output=True, shell=True, check=True)
    os.chdir(chemin_instal_Zyminterne)
    # lancer Zyminterne sur l'acquisition définie
    commande2 = r'Zyminterne.exe -i ' + chemin_Images_input + ' -f ' + chemin_Reconstruction + ' -o ' + chemin_Synthese + ' -s ' + chemin_parametres_statistiques + ' -' + longueur_onde + ' -r ' + chemin_parametres_Interf + ' -d ' + images_reconstruction
    subprocess.run(commande2, capture_output=True, shell=True, check=True)


def selection_dossier_acquisitions():
    global chemin_dossier_acquisitions
    dossier_selectionne = filedialog.askdirectory()
    chemin_dossier_acquisitions = dossier_selectionne
    if chemin_dossier_acquisitions != '':
        bouton_dossier_lot['bg'] = 'green'


def selection_fichier_liste_plaques():
    global liste_plaques_csv
    fichier_selectionne = filedialog.askopenfilename(title="Liste des plaques", filetypes=[("Fichiers excel", "*.xlsx"),
                                                                                           ("Tous les fichiers",
                                                                                            "*.*")])
    liste_plaques_csv = fichier_selectionne
    if liste_plaques_csv != '':
        bouton_liste_plaques['bg'] = 'green'


def get_check_box_POST():
    if_POST = case_POST.get()


def get_check_box_EXPO():
    if_EXPO = case_EXPO.get()


def get_check_box_455():
    if_455 = case_455.get()


def get_check_box_730():
    if_730 = case_730.get()


def selection_fichier_parametres_Interf():
    global chemin_Interf
    fichier_selectionne = filedialog.askopenfilename(title="Interf", filetypes=[("Fichiers texte", "*.txt"),
                                                                                ("Tous les fichiers", "*.*")])
    chemin_Interf = fichier_selectionne
    if chemin_Interf != '':
        bouton_Interf['bg'] = 'green'


def selection_fichier_parametres_Stat():
    global chemin_Stat
    fichier_selectionne = filedialog.askopenfilename(title="Stat", filetypes=[("Fichiers parametrage", "*.ini"),
                                                                              ("Tous les fichiers", "*.*")])
    chemin_Stat = fichier_selectionne
    if chemin_Stat != '':
        bouton_Stat['bg'] = 'green'


def get_check_box_plate_type():
    if_colonne_plate_type = case_plate_type.get()


def selection_fichier_variation_param():
    global chemin_variation_param
    fichier_selectionne = filedialog.askopenfilename(title="Stat", filetypes=[("Fichiers excel", "*.xlsx"),
                                                                              ("Tous les fichiers", "*.*")])
    chemin_variation_param = fichier_selectionne
    if chemin_variation_param != '':
        bouton_variation_param['bg'] = 'green'


def generer_n_uplets(*listes):
    return list(itertools.product(*listes))


def inverser_slash(chaine):
    return chaine.replace('/', '\\')


def remplacer_point_virgule(chaine):
    return chaine.replace('.', ',')


def GifS(chaine):
    if " " in chaine:
        return f'"{chaine}"'
    else:
        return chaine


def lancer_reconstruction():
    threading.Thread(
        target=reconstructions(chemin_variation_param, chemin_instal_Zyminterne, chemin_dossier_acquisitions,
                               chemin_Interf, chemin_Stat, images_reconstruction, case_POST.get(), case_EXPO.get(),
                               case_plate_type.get())).start()


def reconstructions(chemin_variation_param, chemin_instal_Zyminterne, chemin_dossier_acquisitions, chemin_Interf,
                    chemin_Stat, images_reconstruction, if_POST, if_EXPO, if_colonne_plate_type):
    # if une_erreur_a_ete_trouvee:
    #     messagebox.showerror("Erreur", "Un message d'erreur décrivant le problème.")
    # Lecture du fichier excel de variation des paramètres
    try:
        param_xlsx = pd.read_excel(chemin_variation_param)
    except:
        messagebox.showerror("Erreur", "fichier variation_parametres.xlsx non trouvé\nou mauvais format")
    param_xlsx_np = np.array(param_xlsx)
    if not (param_xlsx_np[0, 0] == 'h0' and param_xlsx_np[25, 0] == 'brsd' and param_xlsx_np[27, 0] == 'MinVolume' and
            param_xlsx_np[36, 0] == 'DiameterDefinition' and len(param_xlsx_np[:, 0] == 37)):
        messagebox.showerror("Erreur", "fichier variation_parametres.xlsx au mauvais format")
    nb_variation_max = np.shape(param_xlsx_np)
    variation = False
    if nb_variation_max[1] > 1:
        variation = True
        if if_colonne_plate_type:
            conditions = []
            for l in range(nb_variation_max[1] - 1):
                temp = []
                for m in range(nb_variation_max[0]):
                    if not np.isnan(param_xlsx_np[m, l + 1]):
                        temp.append([param_xlsx_np[m, 0], param_xlsx_np[m, l + 1]])
                conditions.append(temp)
            compteur = len(conditions)
        else:
            parametre_variant = []
            for parametre in range(len(param_xlsx_np)):
                valeurs_temp = []
                if not np.isnan(param_xlsx_np[parametre, 1]):
                    j = 1
                    while j < len(param_xlsx_np[parametre]) and not np.isnan(param_xlsx_np[parametre, j]):
                        valeurs_temp.append([param_xlsx_np[parametre, 0], param_xlsx_np[parametre, j]])
                        j += 1
                    parametre_variant.append(valeurs_temp)
            # Matrice qui va contenir toutes les conditions à tester avec toutes les valeurs des paramètres N-uplets
            conditions = generer_n_uplets(*parametre_variant)

            compteur = 1
            for i in range(len(parametre_variant)):
                compteur *= (len(parametre_variant[i]))
            print('Variation de paramètres Interf et/ou Stat : ', compteur, ' conditions à tester')
    else:
        compteur = 1
        print('Aucune variation des paramètres Interf et Stat')

    try:
        liste_acquisitions = pd.read_excel(liste_plaques_csv)
    except:
        messagebox.showerror("Erreur", "fichier liste_plaques.xlsx non trouvé\nou mauvais format")
    liste_acquisitions = np.array(liste_acquisitions)
    # liste_acquisitions = os.listdir(chemin_dossier_acquisitions)
    if len(liste_acquisitions) == 0:
        messagebox.showerror("Erreur", "le dossier d'acquisitions spécifié\nne contient aucune acquisition")
    pe = []
    if if_POST and if_EXPO:
        nb_reconstruction = compteur * len(liste_acquisitions) * 2
        pe = ['post', 'expo']
    elif if_POST and not if_EXPO:
        nb_reconstruction = compteur * len(liste_acquisitions)
        pe = ['post']
    elif if_EXPO and not if_POST:
        nb_reconstruction = compteur * len(liste_acquisitions)
        pe = ['expo']
    else:
        print('Veuillez sélectionner les imageries POST et/ou EXPO')
        messagebox.showerror("Erreur", "Veuillez sélectionner les imageries POST et/ou EXPO")

    if not variation:
        messagebox.showerror("Information", "Aucune variation des paramètres Interf et Stat\n" + str(
            nb_reconstruction) + " reconstruction(s) à effectuer")
    else:
        messagebox.showerror("Information", str(len(conditions)) + " paramétrages différents à tester\n" + str(
            nb_reconstruction) + " reconstruction(s) à effectuer")

    chemin_parametres_Interf = inverser_slash(chemin_Interf)
    chemin_parametres_statistiques = inverser_slash(chemin_Stat)

    longueur_onde_boucle = ''
    with open(chemin_parametres_Interf, 'r') as fichier_Interf:
        lignes_Interf = fichier_Interf.read()
    parametres = lignes_Interf.split()
    for j in range(len(parametres) - 1):
        # Détection de la longueur d'onde utilisée
        if parametres[j] == '-l':
            longueur_onde_boucle = parametres[j + 1]
    if variation:
        kompt = 0
        for condition_test in range(len(conditions)):
            for acquisition in range(len(liste_acquisitions)):
                for PE in pe:
                    chemin_Images_input = inverser_slash(chemin_dossier_acquisitions) + '\\' + liste_acquisitions[
                        acquisition, 0] + '\\' + PE + '\\Images'
                    nom_dossier_reconstruction = ''
                    for i in range(len(conditions[condition_test])):
                        if conditions[condition_test][i][0] in parametres_int:
                            nom_dossier_reconstruction += conditions[condition_test][i][0] + '=' + str(
                                int(conditions[condition_test][i][1])) + '_'
                        elif conditions[condition_test][i][0] in parametres_float:
                            nom_dossier_reconstruction += conditions[condition_test][i][0] + '=' + str(
                                conditions[condition_test][i][1]) + '_'
                        elif conditions[condition_test][i][0] in parametres_str:
                            nom_dossier_reconstruction += conditions[condition_test][i][0] + '=' + str(
                                conditions[condition_test][i][1]) + '_'
                    nom_dossier_reconstruction = nom_dossier_reconstruction[:-1]
                    chemin_Reconstruction = inverser_slash(chemin_dossier_acquisitions) + '\\' + liste_acquisitions[
                        acquisition, 0] + '\\' + PE + '\\' + nom_dossier_reconstruction
                    if not os.path.exists(chemin_Reconstruction):
                        os.makedirs(chemin_Reconstruction)
                    chemin_Synthese = chemin_Reconstruction + '\\Synthese'
                    if not os.path.exists(chemin_Synthese):
                        os.makedirs(chemin_Synthese)
                    images_reconstruction_boucle = images_reconstruction
                    # détection des paramètres Interf ou Stat à modifier
                    param_Interf = []
                    param_Stat = []
                    for i in range(len(conditions[condition_test])):
                        if conditions[condition_test][i][0] in parametres_interf:
                            param_Interf.append(conditions[condition_test][i])
                        if conditions[condition_test][i][0] in parametres_stat:
                            param_Stat.append(conditions[condition_test][i])
                    if not os.path.exists(chemin_Reconstruction + '\\Parametrage'):
                        os.makedirs(chemin_Reconstruction + '\\Parametrage')
                    # génération fichier Interf
                    if len(param_Interf) != 0:
                        # Lire le contenu du fichier original
                        with open(chemin_parametres_Interf, 'r') as fichier_Interf:
                            lignes_Interf = fichier_Interf.read()
                        parametres = lignes_Interf.split()
                        for k in range(len(param_Interf)):
                            for j in range(len(parametres) - 1):
                                # Modifier le paramètre souhaité
                                if '-' + param_Interf[k][0] == parametres[j]:
                                    if param_Interf[k][0] in parametres_int:
                                        parametres[j + 1] = str(int(param_Interf[k][1]))
                                    else:
                                        parametres[j + 1] = str(param_Interf[k][1])
                        # Écrire le contenu modifié dans un nouveau fichier
                        nom_new_fichier_interf = '\\Parametrage\\Interf_'
                        for i in range(len(param_Interf)):
                            if param_Interf[i][0] in parametres_int:
                                nom_new_fichier_interf += param_Interf[i][0] + '=' + str(int(param_Interf[i][1])) + '_'
                            else:
                                nom_new_fichier_interf += param_Interf[i][0] + '=' + str(param_Interf[i][1]) + '_'
                        nom_new_fichier_interf = remplacer_point_virgule(nom_new_fichier_interf[:-1]) + '.txt'
                        nouveau_contenu = " ".join(parametres)
                        with open(chemin_Reconstruction + nom_new_fichier_interf, 'w') as fichier:
                            fichier.write(nouveau_contenu)
                        chemin_parametres_Interf = chemin_Reconstruction + nom_new_fichier_interf
                    # génération fichier Stat
                    if len(param_Stat) != 0:
                        # Lire le contenu du fichier original
                        with open(chemin_parametres_statistiques, 'r') as fichier_Stat:
                            lignes_Stat = fichier_Stat.readlines()
                        for i in range(len(param_Stat)):
                            # Modifier la ligne souhaitée
                            for j in range(len(lignes_Stat)):
                                if '=' in lignes_Stat[j]:
                                    if param_Stat[i][0] == lignes_Stat[j].split("=")[0]:
                                        if param_Stat[i][0] in parametres_int:
                                            lignes_Stat[j] = param_Stat[i][0] + '=' + str(int(param_Stat[i][1])) + '\n'
                                        else:
                                            lignes_Stat[j] = param_Stat[i][0] + '=' + str(param_Stat[i][1]) + '\n'
                                            # Écrire le contenu modifié dans un nouveau fichier
                        nom_new_fichier_stat = '\\Parametrage\\Stat_'
                        for i in range(len(param_Stat)):
                            if param_Stat[i][0] in parametres_int:
                                nom_new_fichier_stat += param_Stat[i][0] + '=' + str(int(param_Stat[i][1])) + '_'
                            else:
                                nom_new_fichier_stat += param_Stat[i][0] + '=' + str(param_Stat[i][1]) + '_'
                        nom_new_fichier_stat = remplacer_point_virgule(nom_new_fichier_stat[:-1]) + '.ini'
                        with open(chemin_Reconstruction + nom_new_fichier_stat, 'w') as fichier:
                            fichier.writelines(lignes_Stat)
                        chemin_parametres_statistiques = chemin_Reconstruction + nom_new_fichier_stat
                    kompt += 1
                    ma_variable.set(str(kompt) + " reconstruction(s) sur " + str(nb_reconstruction))
                    fenetre.update_idletasks()
                    print(kompt, ' reconstruction(s) sur ', nb_reconstruction)
                    Zyminterne(chemin_instal_Zyminterne, GifS(chemin_Images_input), GifS(chemin_parametres_Interf),
                               GifS(chemin_parametres_statistiques), GifS(chemin_Reconstruction), GifS(chemin_Synthese),
                               longueur_onde_boucle, images_reconstruction_boucle)

    else:
        kompt = 0
        for acquisition in range(len(liste_acquisitions)):
            for PE in ('post', 'expo'):
                chemin_Images_input = inverser_slash(chemin_dossier_acquisitions) + '\\' + liste_acquisitions[
                    acquisition, 0] + '\\' + PE + '\\Images'
                nom_dossier_reconstruction = 'Reconstruction_test'
                chemin_Reconstruction = inverser_slash(chemin_dossier_acquisitions) + '\\' + liste_acquisitions[
                    acquisition, 0] + '\\' + PE + '\\' + nom_dossier_reconstruction
                if not os.path.exists(chemin_Reconstruction):
                    os.makedirs(chemin_Reconstruction)
                chemin_Synthese = chemin_Reconstruction + '\\Synthese'
                if not os.path.exists(chemin_Synthese):
                    os.makedirs(chemin_Synthese)
                images_reconstruction_boucle = images_reconstruction
                kompt += 1
                ma_variable.set(str(kompt) + " reconstruction(s) sur " + str(nb_reconstruction))
                fenetre.update_idletasks()
                print(kompt, ' reconstruction(s) sur ', nb_reconstruction)
                Zyminterne(chemin_instal_Zyminterne, GifS(chemin_Images_input), GifS(chemin_parametres_Interf),
                           GifS(chemin_parametres_statistiques), GifS(chemin_Reconstruction), GifS(chemin_Synthese),
                           longueur_onde_boucle, images_reconstruction_boucle)


# fenêtre Tkinter
fenetre = tk.Tk()
fenetre.title("ZymBatch")
fenetre.geometry("300x500")
# fenetre.iconbitmap(r'C:\Users\PCP_ZYMOPTIQ50\Desktop\ZymBatch\icone.ico')

# listes de tous les boutons
bouton_dossier_lot = tk.Button(fenetre, text="Dossier d'acquisition", command=selection_dossier_acquisitions)
bouton_dossier_lot.pack(pady=20)
bouton_liste_plaques = tk.Button(fenetre, text="liste des plaques", command=selection_fichier_liste_plaques)
bouton_liste_plaques.pack(pady=20)
case_POST = tk.IntVar()
case_EXPO = tk.IntVar()
checkbox_POST = tk.Checkbutton(fenetre, text="POST", variable=case_POST, command=get_check_box_POST)
checkbox_POST.pack()
checkbox_EXPO = tk.Checkbutton(fenetre, text="EXPO", variable=case_EXPO, command=get_check_box_EXPO)
checkbox_EXPO.pack()
bouton_Interf = tk.Button(fenetre, text="Interf", command=selection_fichier_parametres_Interf)
bouton_Interf.pack(pady=20)
bouton_Stat = tk.Button(fenetre, text="Stat", command=selection_fichier_parametres_Stat)
bouton_Stat.pack(pady=20)
bouton_variation_param = tk.Button(fenetre, text="Variation des paramètres", command=selection_fichier_variation_param)
bouton_variation_param.pack(pady=20)
case_plate_type = tk.IntVar()
checkbox_plate_type = tk.Checkbutton(fenetre, text="colonne = plate-type ?", variable=case_plate_type,
                                     command=get_check_box_plate_type)
checkbox_plate_type.pack()
bouton_lancer_reconstruction = tk.Button(fenetre, text="Lancer les reconstructions", bg="red",
                                         command=lancer_reconstruction)
bouton_lancer_reconstruction.pack(pady=20)

# Créer une variable de contrôle
ma_variable = tk.StringVar()
ma_variable.set(" ")
# Créer un label pour afficher la variable
label = tk.Label(fenetre, textvariable=ma_variable)
label.pack(pady=20)

# Lancer la boucle principale Tkinter
fenetre.mainloop()