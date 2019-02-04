# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 13:48:18 2018

@author: hanc
"""
import os, glob
import cv2

def save_faces(cascade, imgname):
    #img = cv2.imread(os.getcwd().join(imgname))
    print(imgname)
    img = cv2.imread(imgname)
    file = os.path.splitext((os.path.basename(f)))[0]#get just the file name
    for i, face in enumerate(cascade.detectMultiScale(img)): 
        x, y, w, h = face
        try:
            sub_face = img[y-10:y + h + 20, x-10:x + w +10]
        except:
            sub_face = img[y-30:y + h + 20, x-10:x + w +10]
        #cv2.resize(sub_face, (200,350))
        cv2.imwrite(os.path.join("faces", "{}.jpg".format(file)), sub_face)
        

if __name__ == '__main__':
    face_cascade = 'haarcascade_frontalface_default.xml'
    cascade = cv2.CascadeClassifier(face_cascade)
    # Iterate through files
    for f in glob.iglob('Input/**/*.jpg', recursive=True):  
        save_faces(cascade, f)
        
    