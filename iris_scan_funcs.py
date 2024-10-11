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



def expect_and_send(sendValue):
    child.expect("Enter your choice: ")
    child.sendline(sendValue)


def tillYourEyes():

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


    expect_and_send("5")


    # Parameters for capturing process
    # Capture mode: 
    #   1. IDDK_TIMEBASED (default) 
    #   2. IDDK_FRAMEBASED
    # Enter your choice: 


    expect_and_send("1")


    # Enter the duration since iris detected (from 1 to 600 seconds, enter for 3): 5

    child.expect(r"Enter the duration since iris detected \(from 1 to 600 seconds, enter for 3\): ")
    child.sendline("5")

    # Quality mode: 
    #   1. Normal (default)
    #   2. High 
    #   3. Very High
    # Enter your choice:

    expect_and_send("3")

    # Enable auto led? 
    #   1. Yes (default)
    #   2. No
    # Enter your choice:


    expect_and_send("1")

    child.expect("Put your eyes in front of the camera")
    print("""Put your eyes in front of the camera
        Scanning for eyes............................""")



def save_images():  
    # Do you want to get the result image? 
    #   1. No (default)
    #   2. Yes
    # Enter your choice: 2
    expect_and_send("2")

    # Select image kind: 
    #   1. Original Image - K1 (default) 
    #   2. VGA Image - K2 
    #   3. Cropped Image - K3
    #   4. Cropped and Masked Image - K7
    # Enter your choice:

    expect_and_send("1")

    # Select image format: 
    #   1. Mono JP2 Image (default)
    #   2. Mono Raw Image
    #   3. IriTech JP2 Image
    #   4. IriTech Raw Image
    # Enter your choice: 1

    expect_and_send("1")

    # Enter compress ratio (enter for default): 50

    child.expect("Enter compress .*: ")
    child.sendline("50")

    # Do you want to get result ISO image: 
    #   1. No (default)
    #   2. Yes
    # Enter your choice:

    expect_and_send("1")






def check_similarity(path1,path2):

    captured_image_path = path1
    original_image = path2

    imageA = cv2.imread(captured_image_path)    
    
    imageB = cv2.imread(original_image)
    
    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = ssim(grayA, grayB, full=True)
    print(score)
    diff = (diff * 255).astype("uint8")