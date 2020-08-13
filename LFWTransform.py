import os 
import cv2
#from PIL import Image
from numpy import asarray
#from mtcnn.mtcnn import MTCNN
import re
import shutil

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

# extract a single face from a given photograph
def extract_face(filename, required_size=(120, 120)):
	# load image from file
	f = cv2.imread(filename)
	# detect faces in the image
	results = detector.detect_faces(f)
	# extract the bounding box from the first face
	x1, y1, width, height = results[0]['box']
	x2, y2 = x1 + width, y1 + height
	# extract the face
	face = f[abs(y1):abs(y2), abs(x1):abs(x2)]
	# resize pixels to the model size
	image = Image.fromarray(face)
	image = image.resize(required_size)
	face_array = asarray(image)
	return face_array
	
if __name__ == "__main__":
	path = 'CroppedLFW/'
	DIR = 'TransformedLFW/'
	
	N = 0  # total files
	num_files = []
	dirs = []
	for dirpath, dirnames, filenames in os.walk(path):
		N_c = len(filenames)
		N += N_c
		if N_c == 0: continue
		num_files.append(N_c)
		dirs.append(dirpath)
		print("Files in ", dirpath, N_c)
	print("Total Files ",N)
	print(min(num_files), dirs[num_files.index(min(num_files))])
	print(max(num_files), dirs[num_files.index(max(num_files))])
	
	# os.mkdir(path)
	
	# i = 1
	# j = 1
	
	#create the detector, using default weights
	# detector = MTCNN()
	
	# for dirname, dirnames, filenames in os.walk(DIR):
		# for subdirname in sorted(dirnames, key=natural_keys):
			# os.mkdir("%s/s%d" %(path, i))
			# subject_path = os.path.join(dirname, subdirname)
			# for file in os.listdir(subject_path):
				# filepath = os.path.join(dirname, subdirname, file)
				# try:
					# img = extract_face(filepath)
				# except IndexError:
					# continue
				#img = cv2.imread(filepath)
				#img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
				# cv2.imwrite(r"%s/s%d/%d.jpg" % (path, i, j), img)
				# j += 1
			# i += 1
			# j = 1