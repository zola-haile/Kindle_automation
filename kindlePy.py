import pexpect
import csv
import os
import re
import serial
import time
from skimage.metrics import structural_similarity as ssim
import argparse
import imutils
import cv2
from moveServo import moveServo
from iris_scan_funcs import tillYourEyes,expect_and_send, get_images,check_similarity # type: ignore

imgNames=[]

dummyImg=""


# Set the environment variable
os.environ['DYLD_LIBRARY_PATH'] = '/opt/IriTech/IDDK-2000-3.3.1-OSX/demo/source:' + os.environ.get('DYLD_LIBRARY_PATH', '')

# Path to the executable
executable = '/opt/IriTech/IDDK-2000-3.3.1-OSX/demo/source/Iddk2000Demo'

loop=True
list_of_unscanned_iris=[]
number_imgs_taken=0


while loop:

    # Start the process
    child = pexpect.spawn(executable)
    child.logfile = open('pexpect.log', 'wb')

     # Interact with the process
    child.expect("Please press ENTER to continue ...")
    child.sendline("")

    # Reset on open device: 
    #   1. Yes (default)
    #   2. No

    expect_and_send("1")
    
    tillYourEyes()

    loop_to_capture=True
    count=0

    while loop_to_capture:

        index=child.expect(["Error: IDDK_SE_NO_QUALIFIED_FRAME","Error: IDDK_SE_NO_FRAME_AVAILABLE","Do you want to get the result image?"])
        
        if index==0 or index==1:

            tillYourEyes()
            
            loop_to_capture=True
            count+=1
            if count==5:
                # MAIN MENU: Select one of the features below
            #   1. Login
            #   2. Logout
            #   3. Device Management
            #   4. Device & SDK Information
            #   5. Capturing Process
            #   6. Iris Recognition
            #   7. Power Management
            #   8. Recovery (IriShield USB only)
            #   9. Exit
            # Enter your choice:

                expect_and_send("9")

                list_of_unscanned_iris.append(imgName[0])


                with open("unscanned_imgName.csv",'a', newline='') as csvfile:
                    csvwriter=csv.writer(csvfile)

                    csvwriter.writerows(imgName[0])
                print("****  This iris could not be scanned, so it is skiped ***")
                
                
                moveServo("nothing yet")
                break
            continue

        elif index==2:
            loop_to_capture=False

    
    if index==2:
        get_images()
        child.logfile.close()
    

        child=pexpect.spawn(f"mv /opt/IriTech/IDDK-2000-3.3.1-OSX/demo/source/UnknownEyeImage_1.jp2 /Users/czajkademo1/Desktop/pyDemo/saved_images/{imgNames[0]}.jp2")
        print("Process completed.")

        path1=dummyImg
        path2=f"/Users/czajkademo1/Desktop/pyDemo/saved_images/{imgNames[0]}.jp2"

        similarity_score=check_similarity(path1,path2)

        if similarity_score>0.8:
            
            moveServo("nothing yet")
            path1=path2
            imgNames.pop(0)



    number_imgs_taken+=1
    print(f"Number of images scanned so far {number_imgs_taken}.")
    do_continue=input("Enter q to quit; anything else to continue: ")
    if do_continue.lower()!="q":
        loop=True
    else:
        loop=False








fileName_imgName_comparison="imgName_comparison.csv"
fileName_imgName_naming="imgName_naming.csv"


with open(fileName_imgName_comparison,'w', newline='') as csvfile:
    csvwriter=csv.writer(csvfile)

    for item in nameList:
        csvwriter.writerow([item])


with open(fileName_imgName_naming,'w', newline='') as csvfile:
    csvwriter=csv.writer(csvfile)

    for item in imgName:
        csvwriter.writerow([item])



