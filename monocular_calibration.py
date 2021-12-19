import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import glob
import sys
import os
import json 

def monocular_calibration(path='./calibration_images/*.tiff', size_x=6, size_y=9, display=False):
    
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 26, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*9,3), np.float32)
    objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    images = glob.glob(path)
    for fname in images:
        img = cv.imread(fname)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, (9,6), None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray,corners, (13,13), (-1,-1), criteria)
            imgpoints.append(corners)
            # Draw and display the corners
            cv.drawChessboardCorners(img, (9,6), corners2, ret)
            if display:
                plt.imshow(img)
                plt.show()        
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    # calculate average reprojection error
    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
        mean_error += error
    rep_error = mean_error/len(objpoints)
    # calculate optimal new camera matrix and roi
    folder = path[0:-6]
    # read an image
    img = cv.imread(folder+os.listdir(folder)[0])
    h,  w = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 0, (w,h))

    return ret, mtx, dist, rvecs, tvecs, rep_error, newcameramtx, roi

if __name__ == "__main__":
    ret, mtx, dist, rvecs, tvecs, rep_error, newcameramtx, roi = monocular_calibration()

    calib_info = {}
    calib_info['ret'] = ret
    calib_info['mtx'] = mtx
    calib_info['rvecs'] = rvecs
    calib_info['tvecs'] = tvecs
    calib_info['rep_error'] = rep_error
    calib_info['newcameramtx'] = newcameramtx
    calib_info['roi'] = roi
    
    print('\n##########################################################################################################')
    print("Completed. Calibration results saved as npy file")
    print('##########################################################################################################\n')
    np.save('./monocular_calibration_results', calib_info)
    # sanity check 
    # results = np.load('./monocular_calibration_results.npy', allow_pickle=True)
    # print(results)