# -*- coding: utf8 -*-

import cv2
import random
import numpy as np
import csv
import os

def write_csv(f, folder):  
    c = csv.writer(open(f, "wb"))

    SEPARATOR = ";"
    BASE_PATH = folder

    label = 0
    for dirname, dirnames, filenames in os.walk(BASE_PATH):
        for subdirname in dirnames:
            subject_path = os.path.join(dirname, subdirname)
            for filename in os.listdir(subject_path):
                abs_path = "%s/%s" % (subject_path, filename)
                c.writerow(["%s%s%d" % (abs_path, SEPARATOR, label)])
            label = label + 1
            
if __name__ == "__main__":
    holdouts = 100
    n_classes = 100
    training_sample = 13 

    File = "AR.csv"

    write_csv(File, "AR/")

    files = []
    
    with open(File, "rb") as csvfile:
        reader = csv.reader(csvfile, delimiter= ';')
        for line in reader:
            files.append([line[0], line[1]])

    files = np.array(files)

    with open("AR.txt", "wb") as txt:
        for i in range(holdouts):
            training = []
            test = []

            for j in range(0, n_classes):
                temp_arr_rows = np.where(files[:, 1].astype(int) == j)
                #treino_arr = files[temp_arr_rows][5:13]
                #treino_arr = np.append(treino_arr, files[temp_arr_rows][19:24], axis=0)
                treino_arr = random.sample(files[temp_arr_rows], training_sample)
            
                for k in treino_arr:   
                    training.append(k)
                
                test_arr = [l for l in files[temp_arr_rows].tolist() if l not in np.asarray(treino_arr).tolist()]
               
                for k in test_arr:
                    test.append(k)
                    
            training = np.array(training)
            test = np.array(test)

            k = ""
            for j in training:
                if j[1] != k:
                    txt.write("|%s" % j[1])
                txt.write(",%s" % j[0])
                k = j[1]
                
            txt.write(";")
            
            k = ""
            for j in test:
                if j[1] != k:
                    txt.write("|%s" % j[1])
                txt.write(",%s" % j[0])
                k = j[1]
            
            txt.write("\n")
            
       
        
            

        

        
