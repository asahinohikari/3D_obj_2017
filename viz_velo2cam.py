import numpy as np
import matplotlib.pyplot as plt
import cv2

# File path
img_file = r'D:\THESIS\KITTI\3D_obj_2017\data_object_image_2\testing\image_2\000001.png'
velo_file = r'D:\THESIS\KITTI\3D_obj_2017\data_object_velodyne\testing\velodyne\000001.bin'
calib_file = r'D:\THESIS\KITTI\3D_obj_2017\data_object_calib\testing\calib\000001.txt'

# Read image
img = cv2.imread(img_file)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # RGB display

# Read raw data from lidar binary data
pc = np.fromfile(velo_file, dtype=np.float32).reshape((-1, 4))  # Reshape to size Nx4
# pointClouds = pointClouds[0:len(pointClouds):5]  # Remove every 5th point for display speed
pc = pc[:, 0:3]  # Get lidar xyz (front, left, up)

# Read calibration files and extract transform matrix
with open(calib_file,'r') as f:
    calib = f.readlines()
# P2 (size 3x4) for left color camera
P2 = np.matrix([float(x) for x in calib[2].strip('\n').split(' ')[1:]]).reshape(3,4)
# R0_rect (reshape size 3x3 to size 4x4)
R0_rect = np.matrix([float(x) for x in calib[4].strip('\n').split(' ')[1:]]).reshape(3,3)
R0_rect = np.insert(R0_rect,3,values=[0,0,0],axis=0)
R0_rect = np.insert(R0_rect,3,values=[0,0,0,1],axis=1)
# Tr_velo_to_cam (reshape size 3x4 to size 4x4)
Tr_velo_to_cam = np.matrix([float(x) for x in calib[5].strip('\n').split(' ')[1:]]).reshape(3,4)
Tr_velo_to_cam = np.insert(Tr_velo_to_cam,3,values=[0,0,0,1],axis=0)

#######################################################################################################################
# velo2Cam
# velo
velo = np.insert(pc, 3, 1, axis=1).T
velo = np.delete(velo,np.where(velo[0,:]<0),axis=1)
# cam = P2*R0_rect*Tr_velo_to_cam *velo
cam = P2 * R0_rect * Tr_velo_to_cam * velo
cam = np.delete(cam,np.where(cam[2,:]<0)[1],axis=1)
# Normalize 变换为齐次坐标 Get u,v,z
cam[:2] /= cam[2,:]  # x=x/z, y =y/z
#######################################################################################################################

# Filter point out of views
IMG_H,IMG_W,_ = img.shape
u,v,z = cam
u_out = np.logical_or(u<0, u>IMG_W)
v_out = np.logical_or(v<0, v>IMG_H)
outlier = np.logical_or(u_out, v_out)
cam = np.delete(cam,np.where(outlier),axis=1)
x,y,z = cam

# Project the lidar point to the image
plt.figure(figsize=((IMG_W)/72.0,(IMG_H)/72.0),dpi=72.0, tight_layout=True)
plt.axis([0,IMG_W,IMG_H,0])  # Restrict canvas in range
plt.imshow(img)
plt.scatter([x],[y],c=[z],cmap='gist_rainbow',alpha=0.5,s=2)  # Generate color map from depth
# plt.title('000000')

# Save figure
plt.savefig(r"./data_velo2cam/testing/000001.png",bbox_inches='tight')
plt.show()