#! python3
"""
Automatic cropping of faces in images for use with ID card printing

@author: Charles Han
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
            sub_face = img[y-15:y + h + 20, x-10:x + w +10]
        except:
            sub_face = img[y-30:y + h + 20, x-10:x + w +10]
        
        if sub_face.shape[0] > 300 and sub_face.shape[1] > 400:
            sub_face = cv2.resize(sub_face, (300,400))
            
        cv2.imwrite(os.path.join("faces", "{}.jpg".format(file)), sub_face)
        

if __name__ == '__main__':
    face_cascade = 'haarcascade_frontalface_default.xml'
    cascade = cv2.CascadeClassifier(face_cascade)
    # Iterate through files
    for f in glob.iglob('**/*.jpg', recursive=True):  
        save_faces(cascade, f)
        
    