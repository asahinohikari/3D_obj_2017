import numpy as np
import cv2
from PIL import Image

# File path
img_file = r'D:\THESIS\KITTI\3D_obj_2017\data_object_image_2\training\image_2\000001.png'
calib_file = r'D:\THESIS\KITTI\3D_obj_2017\data_object_calib\training\calib\000001.txt'
obj_file = r'D:\THESIS\KITTI\3D_obj_2017\data_object_label_2\training\label_2\000001.txt'

# Read image
img = cv2.imread(img_file)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Read calibration files
with open(calib_file,'r') as f:
    calib = f.readlines()
P2 = np.matrix([float(x) for x in calib[2].strip('\n').split(' ')[1:]]).reshape(3,4)

# Object attributes
class Object3d(object):
    def __init__(self, label_file_line):
        data = label_file_line.split(' ')
        data[1:] = [float(x) for x in data[1:]]

        # extract label, truncation, occlusion
        self.type = data[0]  # 'Car', 'Pedestrian', ...
        self.truncation = data[1]  # truncated pixel ratio [0..1]
        self.occlusion = int(data[2])  # 0=visible, 1=partly occluded, 2=fully occluded, 3=unknown
        self.alpha = data[3]  # object observation angle [-pi..pi]

        # extract 2D bounding box in 0-based coordinates
        self.xmin = data[4]  # left
        self.ymin = data[5]  # top
        self.xmax = data[6]  # right
        self.ymax = data[7]  # bottom
        self.box2d = np.array([self.xmin, self.ymin, self.xmax, self.ymax])

        # extract 3D bounding box information
        self.h = data[8]  # box height
        self.w = data[9]  # box width
        self.l = data[10]  # box length (in meters)
        self.t = (data[11], data[12], data[13])  # location (x,y,z) in camera coord.
        self.ry = data[14]  # yaw angle (around Y-axis in camera coordinates) [-pi..pi]

    def print_object(self):
        print('Type, truncation, occlusion, alpha: %s, %d, %d, %f' % \
              (self.type, self.truncation, self.occlusion, self.alpha))
        print('2d bbox (x0,y0,x1,y1): %f, %f, %f, %f' % \
              (self.xmin, self.ymin, self.xmax, self.ymax))
        print('3d bbox h,w,l: %f, %f, %f' % \
              (self.h, self.w, self.l))
        print('3d bbox location, ry: (%f, %f, %f), %f' % \
              (self.t[0], self.t[1], self.t[2], self.ry))

# Label attribute
def read_label(label_filename):
    lines = [line.rstrip() for line in open(label_filename)]
    objects = [Object3d(line) for line in lines]
    return objects
objects = read_label(obj_file)

# Rotation about the y-axis
def roty(t):
    c = np.cos(t)
    s = np.sin(t)
    # rotation matrix
    return np.array([[c,  0,  s],
                     [0,  1,  0],
                     [-s, 0,  c]])

# Project 3d points to image plane
def project_to_image(pts_3d, P):
    '''
    Usage: pts_2d = projectToImage(pts_3d, P)
      input: pts_3d: nx3 matrix
             P:      3x4 projection matrix
      output: pts_2d: nx2 matrix

      P(3x4) dot pts_3d_extended(4xn) = projected_pts_2d(3xn)
      => normalize projected_pts_2d(2xn)

      <=> pts_3d_extended(nx4) dot P'(4x3) = projected_pts_2d(nx3)
          => normalize projected_pts_2d(nx2)
    '''
    n = pts_3d.shape[0]
    pts_3d_extend = np.hstack((pts_3d, np.ones((n, 1))))
    # print(('pts_3d_extend shape: ', pts_3d_extend.shape))
    pts_2d = np.dot(pts_3d_extend, np.transpose(P))  # nx3
    pts_2d[:, 0] /= pts_2d[:, 2]
    pts_2d[:, 1] /= pts_2d[:, 2]
    return pts_2d[:, 0:2]

# Takes an object and a projection matrix (P) and projects the 3D bounding box into the image plane
def compute_box_3d(obj, P):
    '''
        Returns:
            corners_2d: (8,2) array in left image coord.
            corners_3d: (8,3) array in in rect camera coord.
    '''
    # compute rotational matrix around yaw axis
    Ry = roty(obj.ry)

    # 3D bounding box dimensions
    l = obj.l;
    w = obj.w;
    h = obj.h;

    # 3D bounding box corners
    x_corners = [l / 2, l / 2, -l / 2, -l / 2, l / 2, l / 2, -l / 2, -l / 2];
    y_corners = [0, 0, 0, 0, -h, -h, -h, -h];
    z_corners = [w / 2, -w / 2, -w / 2, w / 2, w / 2, -w / 2, -w / 2, w / 2];

    # rotate and translate 3D bounding box
    corners_3d = np.dot(Ry, np.vstack([x_corners, y_corners, z_corners]))

    # print corners_3d.shape
    corners_3d[0, :] = corners_3d[0, :] + obj.t[0];
    corners_3d[1, :] = corners_3d[1, :] + obj.t[1];
    corners_3d[2, :] = corners_3d[2, :] + obj.t[2];
    # print 'cornsers_3d: ', corners_3d
    # only draw 3d bounding box for objs in front of the camera
    if np.any(corners_3d[2, :] < 0.1):
        corners_2d = None
        return corners_2d, np.transpose(corners_3d)

    # project the 3D bounding box into the image plane
    corners_2d = project_to_image(np.transpose(corners_3d), P);
    # print 'corners_2d: ', corners_2d
    return corners_2d, np.transpose(corners_3d)

# Draw 3d bounding box in image
def draw_projected_box3d(image, qs, color=(255,255,255), thickness=1):
    '''
        qs: (8,3) array of vertices for the 3d box in following order:
            1 -------- 0
           /|         /|
          2 -------- 3 .
          | |        | |
          . 5 -------- 4
          |/         |/
          6 -------- 7
    '''
    qs = qs.astype(np.int32)
    for k in range(0,4):
       # Ref: http://docs.enthought.com/mayavi/mayavi/auto/mlab_helper_functions.html
       i,j=k,(k+1)%4
       # use LINE_AA for opencv3
       cv2.line(image, (qs[i,0],qs[i,1]), (qs[j,0],qs[j,1]), color, thickness)

       i,j=k+4,(k+1)%4 + 4
       cv2.line(image, (qs[i,0],qs[i,1]), (qs[j,0],qs[j,1]), color, thickness)

       i,j=k,k+4
       cv2.line(image, (qs[i,0],qs[i,1]), (qs[j,0],qs[j,1]), color, thickness)
    return image

# Show image with 2D bounding boxes
def show_image_with_boxes(img, objects, show3d=True):
    img2 = np.copy(img)  # for 3D bbox
    for obj in objects:
        if obj.type=='DontCare':continue
        box3d_pts_2d, box3d_pts_3d = compute_box_3d(obj, P2)
        img2 = draw_projected_box3d(img2, box3d_pts_2d)
    if show3d:
        Image.fromarray(img2).show()
        cv2.imwrite(r"./data_3DBB/training/000001.png", cv2.cvtColor(img2, cv2.COLOR_RGB2BGR))

# Image.fromarray(img).show()
show_image_with_boxes(img, objects, True)
