
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 13:48:18 2018

face cropping of passport/ID photos with optional brightness enhancement

@author: Charles Han
"""
import os, glob, sys
import cv2
from PIL import Image, ImageEnhance

# ask yes/no question and return True/false
def query_yes_no(question):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
   
    prompt = " [y/n] "
    
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


# Return brightness of image file (0-255 , black to white)
def get_brightness(image, show_steps):
    orig = image.copy()
    grayimg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # apply a Gaussian blur to the image then find the brightest region with radius
    radius = 11
    grayimg = cv2.GaussianBlur(grayimg, (radius, radius), 0)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(grayimg)

    
    # display the first brightest region
    if show_steps:
        cv2.circle(grayimg, maxLoc, radius, (0, 255, 255 ), 2)
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
def find_face(cascade, imgname, output_folder, show_steps):
    #read image 
    #img = cv2.imread(os.getcwd().join(imgname))
    img = cv2.imread(imgname)
    
    #file = os.path.splitext((os.path.basename(imgname)))[0]#get just the file name
    #for i, face in enumerate(cascade.detectMultiScale(img)): 
    for i, face in enumerate(cascade.detectMultiScale(img, 1.3, 5)):   
        x, y, w, h = face
                
        # display the face found
        if show_steps:
            img2 = img.copy()
            cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.imshow('Face(s) found',img2)
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
            cv2.imwrite(os.path.join(output_folder, "{}_{}.jpg".format(file_name, i)), crop_face)
        else:   
            cv2.imwrite(os.path.join(output_folder, "{}.jpg".format(file_name)), crop_face)
            
        #return crop_face
        

if __name__ == '__main__':
    
    input_folder = 'Input images'
    output_folder = 'Output faces'
    
    face_cascade = 'haarcascade_frontalface_default.xml'
    #eye_cascade = 'haarcascade_eye.xml'
    print("Face identification and cropping with brightness enhancement by Charles Han")
    print("temporary image, temp_img.jpg will be created and used for temporary storage while program is running")
    print("Source code can be found at https://github.com/Charleschehan/Face-crop")
    print("Input folder set to: {}".format(os.path.join(input_folder)))
    print("Output folder set to: {}".format(os.path.join(output_folder)))
    print("Harr cascade file used: {}".format(os.path.join(face_cascade)))
    print("\n")
    adj_brightness = query_yes_no("Enable image brightness enhancement?") 
    show_steps = query_yes_no("Show steps taken (launch viewing window, 0 key to step through)?")
        
    cascade = cv2.CascadeClassifier(face_cascade)
      
    # Iterate through files in Input folder
    for file in glob.iglob('{}/**/*.jpg'.format(input_folder), recursive=True):
        
        #save a temp copy of file
        img = Image.open(file)
        img.save("temp_img.jpg")
        
        #get just the file name
        file_name = os.path.splitext((os.path.basename(file)))[0]
        print(file_name)
        
        if adj_brightness:
            #get brightness of the file
            Brightness = get_brightness(cv2.imread("temp_img.jpg"), show_steps)
            #adjust brightness of file
            if Brightness < 100:
                print("<130")
                adjust_brightness("temp_img.jpg", 2.5)
            elif Brightness < 200:
                print("<200")
                adjust_brightness("temp_img.jpg", 2)
            elif Brightness < 220:
                print("<220")
                adjust_brightness("temp_img.jpg", 1.5)   
        
            get_brightness(cv2.imread("temp_img.jpg"), show_steps) 
       
        #calls find face function
        find_face(cascade, "temp_img.jpg", output_folder, show_steps)
       
        # cv2.imwrite(os.path.join("Output_faces", "{}.jpg".format(file_name)), face)
        
        #clean up
        os.remove("temp_img.jpg") 
    