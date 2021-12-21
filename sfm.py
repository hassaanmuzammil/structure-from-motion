import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from utils import *


def structure_from_motion(file_directory):
    # get filelists 
    filelists = get_files(file_directory)
    # initialize variables
    iter = 0
    prev_img = None
    prev_kp = None
    prev_desc = None
    display= False
    pts_3d = []
    X = np.array([])
    Y = np.array([])
    Z = np.array([])
    # get intrinsic and distortion matrices (K and mtx used interchangeably)
    mtx, dist, newcameramtx, roi = get_camera_params()
    # set camera pose 0 as origin in world coordinates 
    R_t_0 = np.array([[1,0,0,0], [0,1,0,0], [0,0,1,0]])
    # initialize camera pose 1 
    R_t_1 = np.empty((3,4))
    # calculate projection matrix for camera pose 0
    P1 = np.matmul(mtx, R_t_0)
    # initialize projection matrix for camera pose 1
    P2 = np.empty((3,4))
    for file in filelists:
        # read image as grayscale
        img = cv.imread(file, 0)
        h,  w = img.shape[:2]
        # undistort & crop using roi
        x, y, w, h = roi
        resized_img = cv.undistort(img, mtx, dist, None, newcameramtx)[y:y+h, x:x+w]
        # display image
        if display:
            # original
            plt.figure()
            plt.subplot(1,2,1)
            plt.imshow(img, cmap='gray')
            plt.title('Original Image')
            # corrected
            plt.subplot(1,2,2)
            plt.imshow(resized_img, cmap='gray')
            plt.title('Distortion Correction')
            plt.show()
        # create sift object, detect keypoints and descriptors
        sift = cv.SIFT_create()
        kp, desc = sift.detectAndCompute(resized_img,None)
        # for first frame
        if iter == 0:
            prev_img = resized_img
            prev_kp = kp
            prev_desc = desc
         # for subsequent frames
        else:
            # FLANN algorithm parameters
            FLANN_INDEX_KDTREE = 1
            index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
            search_params = dict(checks=100)
            flann = cv.FlannBasedMatcher(index_params,search_params)
            matches = flann.knnMatch(prev_desc,desc,k=2)
            good = []
            pts1 = []
            pts2 = []
            # ratio test as per David Lowe's SIFT paper to detect good matches
            for i,(m,n) in enumerate(matches):
                # vary the constant in if statement for required matching
                if m.distance < 0.7*n.distance:
                    good.append(m)
                    pts1.append(prev_kp[m.queryIdx].pt)
                    pts2.append(kp[m.trainIdx].pt)
            # show correspondences in the two frames
            kp_img = cv.drawMatches(prev_img, prev_kp, resized_img, kp, good, None,matchColor=[0,255,0], flags=2)
            # display
            if display:
                plt.figure(figsize=(10,10))
                plt.imshow(kp_img)
                plt.show()
                # matching points
            pts1 = np.array(pts1)
            pts2 = np.array(pts2)
            # filter based on horizontal criteria
            pts1,pts2 = filter_points(pts1,pts2,th=50)
            # find the fundamental matrix
            F, mask = cv.findFundamentalMat(pts1,pts2,cv.FM_RANSAC)
            # print("\nThe fundamental matrix \n" + str(F))
            # select only inlier points
            pts1 = pts1[mask.ravel()==1]
            pts2 = pts2[mask.ravel()==1]
            # extract essential matrix
            E = np.matmul(np.matmul(np.transpose(mtx), F), mtx)
            # print("\nThe essential matrix is \n" + str(E))
            # recover new camera pose
            retval, R, t, mask = cv.recoverPose(E, pts1, pts2, mtx)
            # get extrinsic camera matrix
            R_t_1[:3,:3] = np.matmul(R, R_t_0[:3,:3])
            R_t_1[:3, 3] = R_t_0[:3, 3] + np.matmul(R_t_0[:3,:3],t.ravel())
            # get projection matrix
            P2 = np.matmul(mtx, R_t_1)
            # transpose
            pts1 = pts1.T
            pts2 = pts2.T
            # triangulate for 3d world points
            points_3d = cv.triangulatePoints(P1, P2, pts1, pts2)
            points_3d /= points_3d[3]
            # calculate reprojection error
            opt_variables = np.hstack((P2.ravel(), points_3d.ravel(order="F")))
            num_points = len(pts2[0])
            rep_error = rep_error_fn(opt_variables, pts2, num_points)
            # print("\nAverage Reprojection Error \n" + str(rep_error))
        # increment iterator
        iter += 1
    # plot point cloud
    plot_3d_matplotlib(points_3d[0:3])
    return points_3d

if __name__ == "__main__":
    # sys args
    argv = sys.argv[1:]
    short_options = "i"
    long_otions = ["images"]
    try:
        options, args = getopt.getopt(argv, short_options, long_options)
    except:
        print("Error loading arguments")

    for current_argument, current_value in options:
        if current_argument in ['-i', '--images']:
            path = current_value
    # Run      
    structure_from_motion(path)
