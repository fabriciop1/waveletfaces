# -*- coding: utf8 -*-

import os
import math
import cv2
import pywt
import csv
import mlpy
import warnings
import timeit
import numpy as np
from Util import Util
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


def waveletfaces_method():

    nn = KNeighborsClassifier(n_neighbors=1)                                                # Classificador 1NN
    gnb = GaussianNB()                                                                      # Classificador Gaussian Naive Bayes
    svc = LinearSVC()
    lda = LinearDiscriminantAnalysis()
    
    taxas_acerto_knn = []
    taxas_acerto_gnb = []
    taxas_acerto_svc = []
    taxas_acerto_lda = []
    
    with open(File, "rb") as csvfile:
        reader = csv.reader(csvfile, delimiter='\n')
        for line in reader:   # each holdout
            treino = []
            teste = []
            imgs_treino = []
            imgs_teste = []
            img = []
            classes_treino = []
            classes_teste = []
            
            lista = line[0].split(";")
            l = lista[0].split("|")
            l.remove("")

            for i in l:
                treino.append(i.split(","))

            l = lista[1].split("|")
            l.remove("")

            for i in l:
                teste.append(i.split(","))

            treino = np.array(treino)
            teste = np.array(teste)
           
            for f in treino:
                for j in f[1:]:
                    j = j.replace("/", "//")
                    with open("%s//%s" %(directory, j), "rb") as csvfile:
                        reader = csv.reader(csvfile, delimiter = ";")
                        for line in reader:
                            img.append(line)
                    imgs_treino.append(np.array(img).flatten())
                    classes_treino.append(f[0])
                    img = []
           
            for f in teste:
                for j in f[1:]:
                    j = j.replace("/", "//")
                    with open("%s//%s" %(directory, j), "rb") as csvfile:
                        reader = csv.reader(csvfile, delimiter = ";")
                        for line in reader:
                            img.append(line)
                    imgs_teste.append(np.array(img).flatten())
                    classes_teste.append(f[0])
                    img = []
    
            imgs_treino = np.array(imgs_treino, dtype=np.float)
            imgs_teste = np.array(imgs_teste, dtype=np.float)
            classes_teste = np.array(classes_teste)
            classes_treino = np.array(classes_treino)
            
            svc.fit(imgs_treino, classes_treino)                                     
            preds = svc.predict(imgs_teste)
            
            taxas_acerto_svc.append(util.getRealAccuracy(classes_teste, preds.astype(str)))
           
            gnb.fit(imgs_treino, classes_treino)
            preds = gnb.predict(imgs_teste)

            taxas_acerto_gnb.append(util.getRealAccuracy(classes_teste, preds.astype(str)))
        
            nn.fit(imgs_treino, classes_treino)
            preds = nn.predict(imgs_teste)
            
            taxas_acerto_knn.append(util.getRealAccuracy(classes_teste, preds.astype(str)))

            lda.fit(imgs_treino, classes_treino)
            preds = lda.predict(imgs_teste)

            taxas_acerto_lda.append(util.getRealAccuracy(classes_teste, preds.astype(str)))
            
    return taxas_acerto_knn, taxas_acerto_gnb, taxas_acerto_svc, taxas_acerto_lda 
    
if __name__ == "__main__":
    start_time = timeit.default_timer()
    base = "GTech"
    
    File = "Waveletfaces LRC//Treino e Teste - 25-75//%s-25.txt" % base
    dirs = ["%s_waveletfaces_lvl3_coif1" % base, "%s_waveletfaces_lvl3_db3" % base, "%s_waveletfaces_lvl3_db4" % base, "%s_waveletfaces_lvl3_haar" % base, "%s_waveletfaces_lvl3_rbio2.2" % base,
            "%s_waveletfaces_lvl3_sym2" % base, "%s_waveletfaces_lvl3_sym4" % base]

    for i in dirs:
        directory = "WaveletFaces LRC//Bases Wavelet//%s//%s" %(base, i)
    
        util = Util()
    
        taxas_acerto_knn, taxas_acerto_gnb, taxas_acerto_svc, taxas_acerto_lda = waveletfaces_method()

        print "\nFile - ", i
        print "\nSupport Vector Classification: \n", "Media: %.5f" % (np.mean(np.array(taxas_acerto_svc)) / 100.0), "\tDesvio Padrao: %.5f" % (np.std(np.array(taxas_acerto_svc)) / 100.0)
        print "\nGaussian Naive Bayes: \n",          "Media: %.5f" % (np.mean(np.array(taxas_acerto_gnb)) / 100.0), "\tDesvio Padrao: %.5f" % (np.std(np.array(taxas_acerto_gnb)) / 100.0)
        print "\nKNN: \n",                           "Media: %.5f" % (np.mean(np.array(taxas_acerto_knn)) / 100.0), "\tDesvio Padrao: %.5f" % (np.std(np.array(taxas_acerto_knn)) / 100.0)
        print "\nLDA: \n",                           "Media: %.5f" % (np.mean(np.array(taxas_acerto_lda)) / 100.0), "\tDesvio Padrao: %.5f" % (np.std(np.array(taxas_acerto_lda)) / 100.0)
        
        print "\nTime: ", (timeit.default_timer() - start_time) / 60.0, " mins"
    
    
