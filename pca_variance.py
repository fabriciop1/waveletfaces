# -*- coding: utf8 -*-

import cv2
import pywt
import csv
import warnings
import numpy as np
from numpy import cumsum
from Util import Util
from sklearn.svm import LinearSVC
from sklearn.decomposition import PCA
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams.update({'font.size': 19})

files = ["AR.txt", "YaleB.txt", "ORL.txt", "GTech.txt", "faces95.txt"]
Y = []
for File in files:
    with open(File, "rb") as csvfile:	# File contem os conjuntos de treino e teste. Cada linha -> um holdout
        reader = csv.reader(csvfile, delimiter='\n')
        X = []
        
        for line in reader:  # cada holdout
            nn = KNeighborsClassifier(n_neighbors=1, metric="euclidean")   # 1-NN, distancia euclideana
            gnb = GaussianNB()  				  # classificador GNB (parametros default)
            svc = LinearSVC()					  # classificador SVM (parametros default)
            rfc = RandomForestClassifier()		  # classificador RFC (parametros default)

            treino, teste = [], []
            classes_treino, classes_teste = [], []
            # separando os conjuntos de treino e teste #
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
            #########
            training_imgs, test_imgs = [], []

            for row in training:   # Aplicacao do Waveletfaces nas imagens de treino
                    for f in row[1:]:
                        img = cv2.imread(f) # carrega a imagem 
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # conversao para escala de cinza
                        training_imgs.append(img.flatten())	# mantido apenas a aproximacao
                        classes_treino.append(row[0])

            for row in test:	# Aplicacao do Waveletfaces nas imagens de teste
                    for f in row[1:]:
                        img = cv2.imread(f)
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)	     # conversao para escala de cinza
                        test_imgs.append(img.flatten())	         # Imagem de aproximacao mantida
                        classes_teste.append(row[0])
                        
            pca_m = PCA(n_components = 50)
            pca_m.fit(training_imgs)			
            print sum(pca_m.explained_variance_ratio_)
            X.append(pca_m.explained_variance_ratio_)
          
            #training_imgs = pca_m.transform(training_imgs)
            #test_imgs = pca_m.transform(test_imgs)
            
        #print np.mean(np.array(v))
        X = np.matrix(X)
        means = X.mean(0)
        soma = np.asarray(cumsum(means)).reshape(-1)
        Y.append(soma)
        
plt.plot(range(1,51), Y[1], 'ro', label = "Yale B")
plt.plot(range(1,51), Y[1], 'r-')
plt.plot(range(1,51), Y[0], 'b^', label = "AR")
plt.plot(range(1,51), Y[0], 'b-')
plt.plot(range(1,51), Y[2], 'gs', label = "ORL")
plt.plot(range(1,51), Y[2], 'g-')
plt.plot(range(1,51), Y[4], 'c8', label = "Essex")
plt.plot(range(1,51), Y[4], 'c-')
plt.plot(range(1,51), Y[3], 'yp', label = "GTech")
plt.plot(range(1,51), Y[3], 'y-')

plt.ylabel('Porcentagem de Variancia')
plt.xlabel('Numero de Componentes')
plt.legend()

print Y[0][-1], Y[1][-1], Y[2][-1], Y[3][-1], Y[4][-1]

plt.show()
