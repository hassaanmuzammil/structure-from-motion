# structure-from-motion

Date: 19/12/21                                   
Author: Hassaan Muzammil

For monocular/stereo image capture, run the following command:                                         
```
python3 <monocular/stereo>_capture.py
```  
This will create a <monocular/stereo>_ images folder where the frames are saved.                  
Make sure to get the serial number of the basler cams working. 

  
To calibrate camera, point to the path containing the checker pattern images and run the following command:                                                               
```
python3 monocular_calibration.py
```     
Calibration results will be saved as npy file.  
  
To run SfM, pass the path argument which is the images directory.                         
```
python3 sfm.py --path=<images_folder>
```                               


Pipeline Evaluation

Image Undistortion
![Figure_1](https://user-images.githubusercontent.com/52124348/146899997-bc4a4c6e-dffd-4cd1-a2e8-002c048a075c.png)
Dense Feature Matching
![Figure_2](https://user-images.githubusercontent.com/52124348/146900054-34a47965-c6b1-4b4c-b35f-4c225cc8daa5.png)
Scaled Reconstruction
![Figure_3](https://user-images.githubusercontent.com/52124348/146898848-0e58baae-1088-48e2-ad61-8d097aae34c6.png)

