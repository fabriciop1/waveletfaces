# -*- coding: utf8 -*-

import os
import shutil
import random
import numpy as np 
import cv2

if __name__ == "__main__":
	DIR = 'Youtube_Faces/aligned_images_DB/'
	k = 1
	j = 1
	
	N = 0  # total files
	# i = 0
	num_files = []
	dirs = []
	for dirpath, dirnames, filenames in os.walk(DIR):
		N_c = len(filenames)
		N += N_c
		if N_c == 0: continue
		num_files.append(N_c)
		dirs.append(dirpath)
		print "Files in ", dirpath, N_c
	print "Total Files ",N
	print min(num_files), dirs[num_files.index(min(num_files))]
	print max(num_files), dirs[num_files.index(max(num_files))]
	#print np.random.choice([1,2,3,4,5,6], 4, replace=False)
	# os.mkdir("Youtube_Faces/resized_images")
	# for dirname, dirnames, filenames in os.walk(DIR):
		# for subdirname in dirnames:
			# os.mkdir("Youtube_Faces/resized_images/s%d" % (k))
			# subject_path = os.path.join(dirname, subdirname)
			# for i in os.listdir(subject_path):
				# img = cv2.imread(os.path.join(subject_path, i))
				# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
				# img = cv2.resize(img, (313,313))
				# cv2.imwrite("Youtube_Faces/resized_images/s%d/%d.jpg" % (k, j), img)
				# print np.array(img).shape
				# j+=1
			# k += 1
			# j = 1
			# if 150 <= len(os.listdir(subject_path)) <= 500:
				# files = [os.path.join(subject_path, f).replace('\\','/') for f in os.listdir(subject_path) if os.path.isfile(os.path.join(subject_path, f))]
				# random_files = np.random.choice(files, int(len(files)*.40), replace=False)
				# for i in random_files:
					# os.remove(i)
			# else: continue
				
			
			# for i in os.listdir(subject_path_2):
				# subject_path_1 = os.path.join(dirname, subdirname, i)
				# for j in os.listdir(subject_path_1):
					# subject_path = os.path.join(dirname, subdirname, i, j)
					# shutil.move(subject_path, subject_path_2 + "/")
				# try:
					# os.rmdir(subject_path_1)
				# except WindowsError:
					# continue
				
				# shutil.rmtree(subject_path_1)
				# print subject_path
				# print subject_path
				