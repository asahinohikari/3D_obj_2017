import numpy as np
import mayavi.mlab as mlab

# File path
velo_file = r'D:\THESIS\KITTI\3D_obj_2017\data_object_velodyne\testing\velodyne\000001.bin'

# Read raw data from lidar binary data
pc = np.fromfile(velo_file, dtype=np.float32).reshape((-1, 4))  # Reshape to size Nx4
# pc = pointClouds[0:len(pc):5]  # Remove every 5th point for display speed
pc = pc[:, 0:3]  # Get lidar xyz (front, left, up)

# Draw point cloud in 3D space
fig = mlab.figure(figure=None, bgcolor=(0, 0, 0), fgcolor=None, engine=None, size=(1600, 1000))
color = pc[:, 2]
mlab.points3d(pc[:, 0], pc[:, 1], pc[:, 2], color, color=None, mode='point', colormap='nipy_spectral',
                  scale_factor=1, figure=fig)

# Draw origin
mlab.points3d(0, 0, 0, color=(1, 1, 1), mode='sphere', scale_factor=0.2)

# Draw axis
axes = np.array([
    [2., 0., 0., 0.],
    [0., 2., 0., 0.],
    [0., 0., 2., 0.],
], dtype=np.float64)
# mlab.plot3d([0, axes[0, 0]], [0, axes[0, 1]], [0, axes[0, 2]], color=(1, 0, 0), tube_radius=None, figure=fig)
# mlab.plot3d([0, axes[1, 0]], [0, axes[1, 1]], [0, axes[1, 2]], color=(0, 1, 0), tube_radius=None, figure=fig)
# mlab.plot3d([0, axes[2, 0]], [0, axes[2, 1]], [0, axes[2, 2]], color=(0, 0, 1), tube_radius=None, figure=fig)

# Draw fov (todo: update to real sensor spec.)
fov = np.array([  # 45 degree
    [20., 20., 0., 0.],
    [20., -20., 0., 0.],
], dtype=np.float64)

mlab.plot3d([0, fov[0, 0]], [0, fov[0, 1]], [0, fov[0, 2]], color=(1, 1, 1), tube_radius=None, line_width=1,
            figure=fig)
mlab.plot3d([0, fov[1, 0]], [0, fov[1, 1]], [0, fov[1, 2]], color=(1, 1, 1), tube_radius=None, line_width=1,
            figure=fig)

# Draw square region
TOP_Y_MIN = -20
TOP_Y_MAX = 20
TOP_X_MIN = 0
TOP_X_MAX = 40
TOP_Z_MIN = -2.0
TOP_Z_MAX = 0.4

x1 = TOP_X_MIN
x2 = TOP_X_MAX
y1 = TOP_Y_MIN
y2 = TOP_Y_MAX

mlab.plot3d([x1, x1], [y1, y2], [0, 0], color=(0.5, 0.5, 0.5), tube_radius=0.1, line_width=1, figure=fig)
mlab.plot3d([x2, x2], [y1, y2], [0, 0], color=(0.5, 0.5, 0.5), tube_radius=0.1, line_width=1, figure=fig)
mlab.plot3d([x1, x2], [y1, y1], [0, 0], color=(0.5, 0.5, 0.5), tube_radius=0.1, line_width=1, figure=fig)
mlab.plot3d([x1, x2], [y2, y2], [0, 0], color=(0.5, 0.5, 0.5), tube_radius=0.1, line_width=1, figure=fig)

# mlab.orientation_axes()
mlab.view(azimuth=180, elevation=70, focalpoint=[12.0909996, -1.04700089, -2.03249991], distance=62.0, figure=fig)
mlab.savefig(r"./data_3DPC/testing/000001.png")
mlab.show()