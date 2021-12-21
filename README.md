# structure-from-motion

Date: 19/12/21                                   
Author: Hassaan Muzammil

For monocular/stereo image capture, run the following command:                      
This will create a <monocular/stereo>_ images folder where the frames are saved.                  
Make sure to get the serial number of the basler cams working.
```python3 <monocular/stereo>_capture.py```                                           

  
To calibrate camera, point to the path containing the checker pattern images and run the following command:                                                  
Calibration results will be saved as npy file.                       
```python3 monocular_calibration.py```                              
  
To run SfM, pass the path argument which is the images directory.                         
```python3 sfm.py --path=<images_folder>```                               


