# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 13:48:18 2018

Face harvesting from images

@author: Charles Han
"""
import os, glob
import cv2

# face detection
def find_face(cascade, img, output_folder):
    #read image 
    #img = cv2.imread(imgname)
    
    #file = os.path.splitext((os.path.basename(imgname)))[0]#get just the file name
    #for i, face in enumerate(cascade.detectMultiScale(img)): 
    for i, face in enumerate(cascade.detectMultiScale(img, 1.3, 5)):   
        x, y, w, h = face
                
        #crop the face found
        try:
            crop_face = img[y-50:y + h + 45, x-10:x + w +10]
        except:
            print("error cropping face")
            #crop_face = img[y-100:y + h + 45, x-10:x + w +10]
        
        #save each face image, if photo yeild more than one face number the files  
        if i > 0 :
            cv2.imwrite(os.path.join(output_folder, "{}_{}.jpg".format(file_name, i)), crop_face)
        else:   
            cv2.imwrite(os.path.join(output_folder, "{}.jpg".format(file_name)), crop_face)
            
        #return crop_face
        
if __name__ == '__main__':
    
    #set some parameters
    input_folder = 'Input images'
    output_folder = 'Output faces'
    face_cascade = 'haarcascade_frontalface_default.xml'
    #eye_cascade = 'haarcascade_eye.xml'
    
    print("Face identification and cropping with brightness enhancement by Charles Han")
    print("Source code can be found at https://github.com/Charleschehan/Face-crop")
    print("Input folder set to: {}".format(os.path.join(input_folder)))
    print("Output folder set to: {}".format(os.path.join(output_folder)))
    print("Harr cascade file used: {}".format(os.path.join(face_cascade)))
    print("Harvesting faces from input folder ...")
    
    cascade = cv2.CascadeClassifier(face_cascade)
      
    # Iterate through files in Input folder
    for file in glob.iglob('{}/**/*.jpg'.format(input_folder), recursive=True):
        
        #get just the file name
        file_name = os.path.splitext((os.path.basename(file)))[0]
        print(file_name)
        
        #make a copy of the image
        image = cv2.imread(file)
        img = image.copy()
        
        #calls find face function
        find_face(cascade, img, output_folder)
       
        
    