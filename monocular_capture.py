import sys
from getopt import getopt, error
from pypylon import pylon
import cv2
import matplotlib.pyplot as plt
import os
import time 

def monocular_capture(save_dir = './monocular_images/', display=False, save=True):
    # Enumerate devices
    devices = pylon.TlFactory.GetInstance().EnumerateDevices()
    print('\n##########################################################################################################')
    print("Camera Info: ",devices[0].GetFriendlyName())
    print('##########################################################################################################\n')
    # Create first device
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    # Open camera
    camera.Open()
    # Initialize counter
    counter = 1
    # Start capturing images
    print('\n#########################################################################################################')
    print("Capturing Images.... ")
    print('#########################################################################################################\n')
    # camera.StartGrabbingMax(numberOfImagesToGrab)
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    since = time.time()
    # converting to opencv bgr format
    converter = pylon.ImageFormatConverter()
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
    # Loop
    while camera.IsGrabbing():
        try:
            # Grab result
            grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if grabResult.GrabSucceeded():
                # Access the image data.
                img = converter.Convert(grabResult).GetArray()
                # Display the image.
                if display:
                    plt.imshow(img)
                # Save the image.
                if not(os.path.isdir(save_dir)):
                    os.mkdir(save_dir)
                if save:
                    cv2.imwrite(save_dir+str(counter)+'.tiff', img)
            # Release result
            grabResult.Release()
            # Update counter
            counter += 1
        except KeyboardInterrupt:
            break
    # Close camera
    camera.Close()
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
    monocular_capture()


