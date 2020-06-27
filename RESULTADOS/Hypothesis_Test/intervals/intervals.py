# -*- coding: utf8 -*-

import cv2
import numpy as np
import math
import csv
import matplotlib.pyplot as plt

def overlap_hypothesis(f):
    yerr = []
    means = []
    with open(f, "rb") as txtfile:
        reader = csv.reader(txtfile, delimiter='\n')
        for line in reader:
            elements = line[0].split("\t")
            if elements[1] == "-": continue
            wavelet, mean, std = elements[0], float(elements[1]), float(elements[2])
            yerr.append(1.96 * std)
            means.append(mean)

        index_max_mean = means.index(max(means))    
        plt.errorbar(range(len(means)), means, yerr=yerr, mfc="red", capsize=5, capthick=1, fmt='o')
        plt.errorbar(index_max_mean, max(means), yerr= yerr[index_max_mean], mfc="red", capsize=5, capthick=1, fmt='o')
        plt.title("Overlap Method")
        plt.show()

def standard_hypothesis(f):
    lines = []
    yerr = []
    means = []
    pos = []
    count = 0
    with open(f, "rb") as txtfile:
        reader = csv.reader(txtfile, delimiter='\n')
        for line in reader:
            elements = line[0].split("\t")
            if elements[1] == "-": continue
            lines.append(elements)
            #wavelet, mean, std = elements[0], float(elements[1]), float(elements[2])
    lines = np.array(lines)
    for i in range(0, len(lines)):
        for j in range(i+1, len(lines)):
            mean_1, mean_2 = float(lines[i, 1]), float(lines[j, 1])
            std_1, std_2 = float(lines[i, 2]), float(lines[j, 2])
            means.append(mean_1 - mean_2)
            yerr.append(1.96 * math.sqrt(std_1 ** 2 + std_2 ** 2))
            if lines[i,0] == "rbio4.4" or lines[j, 0] == "rbio4.4":
                pos.append(count)
            count += 1

    pos = np.array(pos)
    means = np.array(means)
    yerr = np.array(yerr)
    plt.errorbar(range(len(means)), means, yerr=yerr, mfc="red", capsize=5, capthick=1, fmt='o')
    plt.errorbar(pos, means[pos], yerr=yerr[pos], mfc="red", capsize=5, capthick=2, fmt='o')
    plt.title("Standard Method")
    plt.show()
        
#overlap_hypothesis("AR_BestResult_1-NN_Level3_LDA.txt")
#standard_hypothesis("AR_BestResult_1-NN_Level3_LDA.txt")

#overlap_hypothesis("Essex_BestResult_1-NN_Level5_PCA_LDA.txt")
#standard_hypothesis("Essex_BestResult_1-NN_Level5_PCA_LDA.txt")

#overlap_hypothesis("GTech_BestResult_1-NN_Level5_LDA.txt")
#standard_hypothesis("GTech_BestResult_1-NN_Level5_LDA.txt")

#overlap_hypothesis("ORL_BestResult_1-NN_Level2_PCA_LDA.txt")
#standard_hypothesis("ORL_BestResult_1-NN_Level2_PCA_LDA.txt")

overlap_hypothesis("YaleB_BestResult_1-NN_Level4_LDA.txt")
standard_hypothesis("YaleB_BestResult_1-NN_Level4_LDA.txt")

    
