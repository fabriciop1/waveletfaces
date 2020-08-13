import os
import numpy as np
import cv2

def count(path):
	N = 0  # total files
	num_files = []
	dirs = []
	for dirpath, dirnames, filenames in os.walk(path):
		N_c = len(filenames)
		N += N_c
		if N_c == 0: continue
		if N_c < 10: print "2"
		num_files.append(N_c)
		dirs.append(dirpath)
		#print("Files in ", dirpath, N_c)
	print("Total Files ",N)
	print(min(num_files), dirs[num_files.index(min(num_files))])
	print(max(num_files), dirs[num_files.index(max(num_files))])

def remove_files(path):
	for dirname, dirnames, filenames in os.walk(path):
		for subdirname in dirnames:
			subject_path = os.path.join(dirname, subdirname)
			quant_files = os.listdir(subject_path)
			if len(quant_files) >= 200:
				files = [os.path.join(subject_path, f).replace('\\','/') for f in quant_files if os.path.isfile(os.path.join(subject_path, f))]
				random_files = np.random.choice(files, int(len(files)*.40), replace=False)
				for i in random_files:
					os.remove(i)

	
if __name__ == "__main__":
	path = "CASIA-WebFace/"
	
	count(path)
	#remove_files(path)
	
	# j = 1
	# for dirname, dirnames, filenames in os.walk(path):
		# for subdirname in dirnames:
			# subject_path = os.path.join(dirname, subdirname)
			# for file in os.listdir(subject_path):
				# filepath = os.path.join(dirname, subdirname, file)
				# img = cv2.imread(filepath)
				# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
				# cv2.imwrite(r"%s/%d.jpg" % (subject_path, j), img)
				# os.remove(filepath)
				# j += 1
			# j = 1
	