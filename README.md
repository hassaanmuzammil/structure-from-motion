# structure-from-motion

Date: 19/12/21                                   
Author: Hassaan Muzammil

For monocular/stereo image capture, run the following command:                       
```python3 <type>_capture.py```(type is monocular/stereo)                                             
This will create a <type>_images folder where the frames are saved.           

  
To calibrate camera, point to the path containing the checker pattern images and run the following command:                                                  
```python3 monocular_calibration.py``` 
Calibration results will be saved as npy file.                       
  
To run SfM, pass the path argument which is the images directory.                         
```python3 sfm.py --path=<images_folder>```                               


