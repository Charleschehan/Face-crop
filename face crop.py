# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 13:48:18 2018

Brightness adjustment and face cropping of passport/ID photos

@author: hanc
"""
import os, glob
import cv2
from PIL import Image, ImageEnhance

# Return brightness of image file (0-255 , black to white)
def get_brightness(image):
    orig = image.copy()
    grayimg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # apply a Gaussian blur to the image then find the brightest region with radius
    radius = 11
    grayimg = cv2.GaussianBlur(grayimg, (radius, radius), 0)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(grayimg)

    
    # display the first brightest region
    cv2.circle(grayimg, maxLoc,radius, (255, 255, 0 ), 2)
    cv2.imshow("Brightest region", grayimg)
    cv2.waitKey(0) & 0xFF
    cv2.destroyAllWindows()
    
    
    image = orig.copy()
    print(maxVal)
    return maxVal

# adjust brightness of file
def adjust_brightness(file, brightness):
    img = Image.open(file)
    enhancer = ImageEnhance.Brightness(img)
    
    #enhance brightness
    print('Adjusting brightness by',brightness)
    enhanced_img = enhancer.enhance(brightness)
    enhanced_img.save("temp_img.jpg")
    #return enhanced_im

# face detection
def find_face(cascade, imgname):
    #read image 
    #img = cv2.imread(os.getcwd().join(imgname))
    img = cv2.imread(imgname)
    
    #file = os.path.splitext((os.path.basename(imgname)))[0]#get just the file name
    #for i, face in enumerate(cascade.detectMultiScale(img)): 
    for i, face in enumerate(cascade.detectMultiScale(img, 1.3, 5)):   
        x, y, w, h = face
                
        # display the face found
        img2 = img.copy()
        cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imshow('Pic with squares',img2)
        cv2.waitKey(0) & 0xFF
        cv2.destroyAllWindows()
        
        #crop the face found
        try:
            crop_face = img[y-50:y + h + 45, x-10:x + w +10]
        except:
            print("error cropping face")
            #crop_face = img[y-100:y + h + 45, x-10:x + w +10]
        '''
        #resize the face image
        try:
            cv2.resize(crop_face, (300,380))
        except:
            print("error resizing face")
        '''
        #save each face image, if photo yeild more than one face number the files  
        if i > 0 :
            cv2.imwrite(os.path.join("faces", "{}_{}.jpg".format(file_name, i)), crop_face)
        else:   
            cv2.imwrite(os.path.join("faces", "{}.jpg".format(file_name)), crop_face)
            
        #return crop_face
        

if __name__ == '__main__':
    face_cascade = 'haarcascade_frontalface_default.xml'
    eye_cascade = 'haarcascade_eye.xml'

    cascade = cv2.CascadeClassifier(face_cascade)
      
    # Iterate through files in Input folder
    for file in glob.iglob('Input/**/*.jpg', recursive=True):
        
        #save a temp copy of file
        im = Image.open(file)
        im.save("temp_img.jpg")
        
        #get just the file name
        file_name = os.path.splitext((os.path.basename(file)))[0]
        print(file_name)
        
        #get brightness of the file
        Brightness = get_brightness(cv2.imread("temp_img.jpg"))
        #adjust brightness of file
        if Brightness < 100:
            print("<130")
            adjust_brightness(file, 2.5)
        elif Brightness < 200:
            print("<200")
            adjust_brightness(file, 2)
        elif Brightness < 220:
            print("<220")
            adjust_brightness(file, 1.5)   
        
        get_brightness(cv2.imread("temp_img.jpg")) 
       
       
        find_face(cascade, "temp_img.jpg")
       
        # cv2.imwrite(os.path.join("faces", "{}.jpg".format(file_name)), face)
     
    