import numpy as np
import glob
import plotly
import plotly.graph_objs as go
import matplotlib.pyplot as plt

def get_camera_params(filename='./monocular_calibration_results.npy'):
    """
    Load and return calibration results
    """
    # load file and save required values
    calib_info = np.load(filename, allow_pickle=True)
    mtx = calib_info.item().get('mtx')
    dist = calib_info.item().get('dist')
    newcameramtx = calib_info.item().get('newcameramtx')
    roi = calib_info.item().get('roi')
    # return
    return mtx, dist, newcameramtx, roi

def get_files(file_directory, file_type="tiff"):
    """
    Get all required image files from a directory
    Args:
         file_directory: (string containing the required path)
         file_type: (string containing type of image file)
    Returns:
         file_names: (list of required image files from the directory)
    """
    path = file_directory + "*." + file_type
    filenames = [f for f in glob.glob(path)]
    filenames = sorted(filenames)
    return filenames

def plot_3d_plotly(pts_3d):
    """
    Interactive 3d plot of the reconstructed points wrt camera pose 1
    """
    X,Y,Z = pts_3d
    # Configure Plotly to be rendered inline in the notebook.
    plotly.offline.init_notebook_mode()
    # Configure the trace.
    trace = go.Scatter3d(
        x=X,  # <-- Put your data instead
        y=Y,  # <-- Put your data instead
        z=Z,  # <-- Put your data instead
        mode='markers',
        marker={
            'size': 5,
            'opacity': 1,
        }
    )
    # Configure the layout.
    layout = go.Layout(
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0}
    )
    data = [trace]
    plot_figure = go.Figure(data=data, layout=layout)
    # Render the plot.
    plotly.offline.iplot(plot_figure)

def filter_points(matched_points1, matched_points2, th=50):
    """
    Filters matched points that do not specify the horizontal line criteria. Since, the frame rate is high, 
    matched points in successive frames are expected to be horizontal. 
    Args:
        Two numpy arrays showing corresponding feature matches (x,y) from the two images
    Returns:
        Filtered matched points that satisfy the horizontal criteria
    """
    new_matched_points1 = []
    new_matched_points2 = []
    
    for i in range(len(matched_points1)):
        x1,y1 = (matched_points1[i][0], matched_points1[i][1])
        x2,y2 = (matched_points2[i][0], matched_points2[i][1])
        
        if abs(y2-y1) < th:
            new_matched_points1.append([x1,y1])
            new_matched_points2.append([x2,y2])
        else:
            pass
        
    new_matched_points1 = np.array(new_matched_points1)
    new_matched_points2 = np.array(new_matched_points2)
        
    return new_matched_points1, new_matched_points2

def avg_rep_error(rep_error):
    """
    Calculate average reprojection error for all the 3d triangulated points
    Args:
        rep_error: (list of lists [[x,y]] where x,y represent the reprojection error for a single point)
    Returns:
        average reprojection error in pixels for all the triangulated 3d points
    """
    sum_x = 0
    sum_y = 0
    for x,y in rep_error:
        sum_x = sum_x + abs(x)
        sum_y = sum_y + abs(y)
    
    return [sum_x / len(rep_error), sum_y / len(rep_error)]

def rep_error_fn(opt_variables, points_2d, num_pts):
    """
        Calculate reprojection error from the given camera projection matrices, and 2d pixels
        for each triangulated 3d point
    Args:
        opt_variables: (stacked numpy array of projection matrix and 3d points)
        points_2d: (numpy array of 2d sift keypoints)
        num_points: (int representing total number of keypoints)
    Returns:
        Reprojection error of the 3d reconstruction
    """ 
    
    P = opt_variables[0:12].reshape(3,4)
    point_3d = opt_variables[12:].reshape((num_pts, 4))

    rep_error = []

    for idx, pt_3d in enumerate(point_3d):
        pt_2d = np.array([points_2d[0][idx], points_2d[1][idx]])

        reprojected_pt = np.matmul(P, pt_3d)
        reprojected_pt /= reprojected_pt[2]

        #print("Reprojection Error \n" + str(pt_2d - reprojected_pt[0:2]))
        rep_error.append(list(pt_2d - reprojected_pt[0:2]))
        
    avg_error = avg_rep_error(rep_error)
        
    return avg_error


def plot_3d_matplotlib(pts_3d):
    X, Y, Z = pts_3d
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    # For each set of style and range settings, plot n random points in the box
    # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
    for m, zlow, zhigh in [('o', -50, 50), ('^', -50, 50)]:
        xs = X
        ys = Y
        zs = Z
        ax.scatter(xs, ys, zs, marker=m)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()