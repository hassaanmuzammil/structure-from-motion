import sys
from getopt import getopt, error
from pypylon import pylon
import cv2
import matplotlib.pyplot as plt
import os 
import time

def stereo_capture(save_dir = './stereo_images/', display=False, save=True):
    # Enumerate devices
    cams = []
    for i in pylon.TlFactory.GetInstance().EnumerateDevices():
        cams.append(i)
    print('\n##########################################################################################################')
    print("Cameras Info: ")
    print(cams[0].GetFriendlyName()) 
    print(cams[1].GetFriendlyName())
    print('##########################################################################################################\n')
    # Create first and second devices
    camera_1 = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(cams[0]))
    camera_2 = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(cams[1]))
    # Open cameras
    camera_1.Open()
    camera_2.Open()
    # Initialize counter
    counter = 1
    # Start capturing images with minimal delay
    print('\n#########################################################################################################')
    print("Capturing Images.... ")
    print('#########################################################################################################\n')
    camera_1.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
    camera_2.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
    since = time.time()
    # converting to opencv bgr format
    converter = pylon.ImageFormatConverter()
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
    # Loop
    while camera_1.IsGrabbing() and camera_2.IsGrabbing():
        try:
            # Grab results
            grabResult_1 = camera_1.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            grabResult_2 = camera_2.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if grabResult_1.GrabSucceeded() and grabResult_2.GrabSucceeded():
                # Access the image data
                img_1 = converter.Convert(grabResult_1).GetArray()
                img_2 = converter.Convert(grabResult_2).GetArray()
                # Display the image.
                if display:
                    plt.imshow('right', img_1)
                    plt.imshow('left', img_2)
                # Save the image.
                if not(os.path.isdir(save_dir)):
                    os.mkdir(save_dir)
                if save:
                    cv2.imwrite(save_dir+str(counter)+'_R_.tiff', img_1) #right
                    cv2.imwrite(save_dir+str(counter)+'_L_.tiff', img_2) #left
            # Release results
            grabResult_1.Release()
            grabResult_2.Release()
            # Update counter
            counter += 1
        except KeyboardInterrupt:
            break
    # Close cameras
    camera_1.Close()
    camera_2.Close()
    # Stats
    print('\n##########################################################################################################')
    print("Exiting....")
    print("Total Images Captured: ",counter)
    time_elapsed = time.time() - since
    print('Time Elapsed {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
    print('##########################################################################################################\n')

if __name__ == "__main__":
    # Exit Info
    print('\n##########################################################################################################')
    print('Press Ctrl+C to exit')
    print('##########################################################################################################\n')
    # Run
    stereo_capture()
        