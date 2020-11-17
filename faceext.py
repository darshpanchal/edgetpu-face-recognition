import cv2
import os
import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-g', '--get', required=True,
                    help='Folder path for source pictures.')
parser.add_argument('-s', '--save', required=True,
                    help='Folder path to save extracted faces.')
args = parser.parse_args()

path = args.get
savepath = args.save
files = os.listdir(path)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

for afile in files:
    img = cv2.imread(path + afile)
    print(afile)
    img = cv2.resize(img, (0,0), fx = 0.4, fy = 0.4)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    x,y,w,h = faces[0]
    img = img[y:y+h, x:x+w]
    img = cv2.resize(img, (224,224))
    name1 = savepath + afile
    cv2.imwrite(name1, img)
