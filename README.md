# 3D_obj_2017

## Introduction
KITTI dataset — LiDAR point cloud visualization | LiDAR to image projection | 3D BBox labelling on image
### This program is for learning purposes only.

## Dependencies
Dependencies `numpy`, `matplotlib`, `cv2`, `mayavi` and 'PIL' need to be installed to run the program.
```
numpy == 1.19.5
matplotlib == 3.3.4
opencv-python = 4.6.0
mayavi = 4.7.3
Pillow = 8.4.0
```

## Project Structure
The file structure is as follows: 

```
3D_obj_2017/
├── data_object_image_2/
│   └── testing/
│   └── training/
│       └── image_2/
│           └── 000001.png
├── data_object_velodyne/
│   └── testing/
│   └── training/
│       └── velodyne/
│           └── 000001.bin
├── data_object_calib/
│   └── testing/
│   └── training/
│       └── calib/
│           └── 000001.txt
├── data_object_label_2/
│   └── training/
│       └── label_2/
│           └── 000001.txt
├── data_velo2cam/
│   └── testing/
│       └── 000001.png 
├── viz_velo2cam.py
├── viz_3DPC.py
├── viz_3DBB.py

```

## Dataset
Complete data can be found on [KITTI website](https://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=3d).
Here we only need the following data:
[Download](https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_image_2.zip) left color images of object data set (12 GB)
[Download](https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_image_2.zip) Velodyne point clouds, if you want to use laser information (29 GB)
[Download](https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_calib.zip) camera calibration matrices of object data set (16 MB)
[Download](https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_label_2.zip) training labels of object data set (5 MB)

## Quick Demo

| File                   | Description                                                                                      |
| ---------------------- | ------------------------------------------------------------------------------------------------ |
| `data_velo2cam.py`     | LiDAR point cloud to camera image projection and visualisation.                                  |
| `data_3DBB.py`         | 3D object annotation of the image.                                                               |
| `data_3DPC.py`         | LiDAR point cloud visualization                                                                  |

Run `data_velo2cam.py`
![](./data_velo2cam/testing/000001.png)

Run `data_3DBB.py`
![](./data_3DBB/training/000001.png)

Run `data_3DPC.py`
![](./data_3DPC/testing/000001.png)

## Reference
[[1] Geiger, A., Lenz, P., Stiller, C., & Urtasun, R. (2013). Vision meets robotics: The kitti dataset. The International Journal of Robotics Research, 32(11), 1231-1237.](https://doi.org/10.1177/0278364913491297)

## Author
Xi Chen (X.CHEN-46@student.tudelft.nl)
