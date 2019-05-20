# -*- coding: utf-8 -*-
"""
Created on Tue Apr 08 13:48:18 2019

download database files

@author: Charles Han
"""

import os, glob
import pymssql


def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    filename.replace("\\",".") 
    #print (os.path.join(filename))
    with open(filename, 'wb') as file:
        file.write(data)

def get_files(output_folder):
  
    #--- connect to PALMS ----  
    server = ""
    userName = ""
    dBase = ""
    print("Logging into %s as %s \nPassword:" %(server , userName))
    password = input()

    conn = pymssql.connect(server, userName, password, dBase)
    cursor = conn.cursor()
    
    #--- SQL to get comms ----
    sql = "SELECT InstrumentID, uploadDocumentName, UploadDocument FROM tblInstrumentCommunication WHERE (CommunicationTypeID = 10 AND BriefDescription ='Declaration photo')"
    cursor.execute(sql)

    #--- write output image file ---    
    for row in cursor:
        print('ID = %r' % (row[0],))
        print('Original filename = %r' % (row[1],))
        
        # strip all slashes in filename so it doesn confuse the program file path
        name = row[1].replace("\\","_").replace("/","_")
        print(name)
        
        new_filename = os.path.join(output_folder, str(row[0]) + '-' + name) 
        file = row[2]
       
        write_file(file, new_filename)
            
    #--- close connection to server ---
    conn.close()
    print('saved image')


        
if __name__ == '__main__':
    #set some parameters
    output_folder = 'Files from PALMS'
    
    print("Fetching BLOB (binary) and saving to files by Charles Han")
    print("Output folder set to: {}".format(os.path.join(output_folder)))
        
    #get all images from database
    get_files(output_folder)

