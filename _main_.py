# -*- coding: utf8 -*-
from __future__ import print_function
import cv2
import pywt
import csv
import sys
import os
import time
import timeit
import warnings
import numpy as np
from Util import Util
from sklearn.svm import LinearSVC
from sklearn.decomposition import PCA
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

warnings.filterwarnings("ignore")
#sys.stdout = open(os.devnull, 'w')
if sys.executable.endswith("pythonw.exe"):
    sys.stdout = sys.stdout = None
csv.field_size_limit(sys.maxint)
## REMEMBER: height = number of rows        width = number of columns

def waveletfaces(wavelet, lvl, method_lda, pca):

    taxas_acerto_svc, taxas_acerto_knn, taxas_acerto_gnb, taxas_acerto_rfc  = [], [], [], []

    with open(File, "rb") as csvfile:
        reader = csv.reader(csvfile, delimiter='\n')
        for line in reader:  # each holdout
            nn = KNeighborsClassifier(n_neighbors=1, metric="euclidean")
            gnb = GaussianNB()  
            svc = LinearSVC()
            rfc = RandomForestClassifier()

            treino, teste = [], []
            classes_treino, classes_teste = [], []

            lista = line[0].split(";")
            l = lista[0].split("|")
            l.remove("")

            for i in l:
                treino.append(i.split(","))

            l = lista[1].split("|")
            l.remove("")

            for i in l:
                teste.append(i.split(","))

            training = np.array(treino)
            test = np.array(teste)

            training_imgs = []
            test_imgs = []
			
            print("WAVELETFACES...")
			
            for row in training:
                for f in row[1:]:
                    img = cv2.imread(f)
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    coeffs = pywt.wavedec2(img, wavelet, level=lvl)
                    training_imgs.append(coeffs[0].flatten())
                    classes_treino.append(row[0])
                    print("TRAINING SET... ", row[0])

            for row in test:
                for f in row[1:]:
                    img = cv2.imread(f)
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    coeffs = pywt.wavedec2(img, wavelet, level=lvl)
                    test_imgs.append(coeffs[0].flatten())
                    classes_teste.append(row[0])
                    print("TEST SET... ", row[0])

            training_imgs = np.array(training_imgs)
            test_imgs = np.array(test_imgs)
            classes_treino = np.array(classes_treino)
            classes_teste = np.array(classes_teste)

            print("AFTER WAVELETFACES ", training_imgs.shape)
            print("PCA ...")
			
            if pca:
                if len(training_imgs[0]) < 50:
                    pca_m = PCA(n_components=len(training_imgs[0]))     # Método PCA   PCA reduz para 50 dimensões, caso o resultado do waveletfaces seja dimensão menor que 50, é mantido o valor
                else:
                    pca_m = PCA(n_components=50)
                pca_m.fit(training_imgs)
                training_imgs = pca_m.transform(training_imgs)
                test_imgs = pca_m.transform(test_imgs)
                print("AFTER PCA ", training_imgs.shape)
				
            print("LDA...")    
			
            if method_lda:
                lda = LinearDiscriminantAnalysis(n_components=100)  # Método LDA        Reduz para n_classes - 1 dimensões ou deixa como está caso seja menor
                lda.fit(training_imgs, classes_treino)
                training_imgs = lda.transform(training_imgs)
                test_imgs = lda.transform(test_imgs)
                print("AFTER LDA", training_imgs.shape)
            print("SVC")
            svc.fit(training_imgs, classes_treino)
            preds = svc.predict(test_imgs)
            svc = None
            taxas_acerto_svc.append(util.getRealAccuracy(classes_teste, preds.astype(str)))
            print("GNB")
            gnb.fit(training_imgs, classes_treino)
            preds = gnb.predict(test_imgs)
            gnb = None
            taxas_acerto_gnb.append(util.getRealAccuracy(classes_teste, preds.astype(str)))
            print("NN")
            nn.fit(training_imgs, classes_treino)
            preds = nn.predict(test_imgs)
            nn = None
            taxas_acerto_knn.append(util.getRealAccuracy(classes_teste, preds.astype(str)))
            print("RFC")
            rfc.fit(training_imgs, classes_treino)
            preds = rfc.predict(test_imgs)
            rfc=None
            taxas_acerto_rfc.append(util.getRealAccuracy(classes_teste, preds.astype(str)))

    return taxas_acerto_rfc, taxas_acerto_svc, taxas_acerto_gnb, taxas_acerto_knn

def findBestFamilies(level, pcaM, methodLda):

    classifiers = ["RFC", "KNN", "GNB", "SVC"]
    start_time = timeit.default_timer()
    ##a = pywt.wavelist(kind="discrete")
    a = ['rbio3.1', 'sym3', 'rbio4.4']
##    b = a[:]
##    for i in a:
##        if i == "rbio3.9":
##            break
##        b.remove(i)

    for i in a:
        try:
            wavelet = pywt.Wavelet(i)
            print(i)
            taxas_acerto_rfc, taxas_acerto_svc, taxas_acerto_gnb, taxas_acerto_knn = waveletfaces(wavelet, lvl=level, pca=pcaM, method_lda=methodLda)
            lista_means = [np.mean(np.array(taxas_acerto_rfc)), np.mean(np.array(taxas_acerto_knn)), np.mean(np.array(taxas_acerto_gnb)), np.mean(np.array(taxas_acerto_svc))]
            lista_stds = [np.std(np.array(taxas_acerto_rfc)), np.std(np.array(taxas_acerto_knn)), np.std(np.array(taxas_acerto_gnb)), np.std(np.array(taxas_acerto_svc))]
            writer.writerow(["%s" % i])

            lista = ["%.3f" % elem for elem in taxas_acerto_rfc]
            lista.insert(0, "RFC")
            writer.writerow(lista)
            lista = ["%.3f" % elem for elem in taxas_acerto_knn]
            lista.insert(0, "KNN")
            writer.writerow(lista)
            lista = ["%.3f" % elem for elem in taxas_acerto_gnb]
            lista.insert(0, "GNB")
            writer.writerow(lista)
            lista = ["%.3f" % elem for elem in taxas_acerto_svc]
            lista.insert(0, "SVM")
            writer.writerow(lista)

            for j in range (0, len(lista_means)):
                print("Wavelet Name =", i)
                print("Classifier: %s" % classifiers[j], "Mean: %.2f" % lista_means[j], "%", "DP: %.5f" % lista_stds[j], "%")

        except ValueError as v:
            print("VALUE ERROR - ", i, "Error: ", v)
            continue

    print("Time: %.5f" % ((timeit.default_timer() - start_time)), "secs")

    
if __name__ == "__main__":

    start_time = timeit.default_timer()
    print("Start Time: ", time.ctime())
    util = Util()
    holdouts = 1
    files = ["CASIA.txt"]
    #files = ["AR.txt", "YaleB.txt", "ORL.txt", "GTech.txt", "faces95.txt"]  # bases de dados
    pcaM = [False, True]                   # Waveletfaces + PCA?
    methodLda = [False, True]              # Wavveletfaces + LDA?

    ############################# MELHORES FAMILIAS WAVELET ################################
    for i in range(0, len(files)):
        File = files[i]

        for j in range(4, 6):
            for k in pcaM:
                for l in methodLda: 
                    if k == False or l == False: continue
                    write_file = open("%s_halfTraining_lvl%s_pca_%s_lda_%s.csv" % (File, j, k, l), "wb")
                    writer = csv.writer(write_file, delimiter = ";")
                    print("\nFile -", File, "half treino ||", " level =", j, "|| pcaM =", k, "|| methodLda =", l)
                    findBestFamilies(level=j, pcaM=k, methodLda=l)
                    write_file.close()
                    print("concluded")
                 #   print "\nFile -", File, "25% treino", " level ", j, "pcaM = ", k, "methodLda = ", l
                 #   findBestFamilies(n_classes, level=j, pcaM=k, methodLda=l)
    ########################################################################################
    
