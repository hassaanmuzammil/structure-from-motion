# structure-from-motion

### The purpose of this exercise is to 3D reconstruct a road surface using 2D images acquired from Basler cams. The algorithm used is SfM.

Installing dependencies
```
pip3 install -r requirements.txt
```

For monocular/stereo image capture, run the following command:                                         
```
python3 <monocular/stereo>_capture.py
```  
This will create a <monocular/stereo>\_images folder where the frames are saved.                  
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


### Pipeline Evaluation
<img width="720" height="720" alt="Screenshot 2021-12-21 at 13 52 19" src="https://user-images.githubusercontent.com/52124348/146900413-885f7649-b860-4b1e-911b-9dd74d63fce7.png">
<img width="720" height="720"alt="Screenshot 2021-12-21 at 13 53 50" src="https://user-images.githubusercontent.com/52124348/146900632-f1861e48-ffb1-4da1-9b5e-fb81b0583b6a.png">
<img width="720" height="720" alt="Screenshot 2021-12-21 at 13 54 45" src="https://user-images.githubusercontent.com/52124348/146900751-3de13d4f-d5bd-4ef6-9610-bac788150277.png">

** Note: The 3D point cloud has a tilt as described in https://publications.aston.ac.uk/id/eprint/42346/1/09345528.pdf

**Date: 19/12/21**                             
**Author: Hassaan Muzammil**
