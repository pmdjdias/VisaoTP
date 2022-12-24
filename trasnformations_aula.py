# ***********************************************************************************
# Name:           viewcloud.py
# Revision:
# Date:           30-10-2019
# Author:         Paulo Dias
# Comments:       Viewcloud
#
# images         left1.jpg->left19.jpg
# Revision:
# Libraries:    Python 3.7.5 + openCV 4.1.0
# ***********************************************************************************
import numpy as np
import open3d as o3d
import cv2
import copy

def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    
    o3d.visualization.draw_geometries([ source_temp, target_temp]
                                    # ,zoom=0.4559,
                                    # front=[0.6452, -0.3036, -0.7011],
                                    # lookat=[1.9892, 2.0208, 1.8945],
                                    # up=[-0.2779, -0.9482, 0.1556]                                    
    )


def preprocess_point_cloud(pcd, voxel_size): # try and correct the point cloud to the original position
    print(":: Downsample with a voxel size %.3f." % voxel_size)
    pcd_down = pcd.voxel_down_sample(voxel_size)

    radius_normal = voxel_size * 2
    print(":: Estimate normal with search radius %.3f." % radius_normal)
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=2000))

    radius_feature = voxel_size * 5
    print(":: Compute FPFH feature with search radius %.3f." % radius_feature)
    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=2000))
    return pcd_down, pcd_fpfh

def prepare_dataset(source,target,voxel_size):
    print(":: Load two point clouds and correct pose.")


    trans_init = np.asarray([[0.0, 0.0, 1.0, 0.0], [1.0, 0.0, 0.0, 0.0],
                             [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
    trans_init=np.identity(4)   
    source.transform(trans_init)
    
    draw_registration_result(source, target, np.identity(4))

    source_down, source_fpfh = preprocess_point_cloud(source, voxel_size)
    target_down, target_fpfh = preprocess_point_cloud(target, voxel_size)
    return source_down, target_down, source_fpfh, target_fpfh

def execute_global_registration(source_down, target_down, source_fpfh,
                                target_fpfh, voxel_size):
    distance_threshold = voxel_size * 1.5
    print(":: RANSAC registration on downsampled point clouds.")
    print("   Since the downsampling voxel size is %.3f," % voxel_size)
    print("   we use a liberal distance threshold %.3f." % distance_threshold)
    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh,distance_threshold,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
        4, 
            [o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(distance_threshold)],
        o3d.pipelines.registration.RANSACConvergenceCriteria(100000,100 ))
    return result


#values/meshes to be used
pcd1= o3d.io.read_point_cloud("/home/jose/Documents/UA/VIsao_computador/aula7/depth_Images/filt_office1.pcd")
pcd2= o3d.io.read_point_cloud("/home/jose/Documents/UA/VIsao_computador/aula7/depth_Images/filt_office2.pcd")



pcd1.paint_uniform_color([1, 0.706, 0])
pcd2.paint_uniform_color([0, 0.651, 0.929])
source=pcd1
target=pcd2
voxel_size = 0.5  # means 5cm for the dataset
threshold = 0.05
trans_init = np.identity(4)

draw_registration_result(source, target, trans_init)


reg_p2p = o3d.pipelines.registration.registration_icp(
    source, target, threshold, trans_init,
    o3d.pipelines.registration.TransformationEstimationPointToPoint(),
    o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration = 300000))
# print(reg_p2p)
print("Transformation is:")
print(reg_p2p.transformation)
draw_registration_result(source, target, reg_p2p.transformation)



#commit para o git



# source_down, target_down, source_fpfh, target_fpfh = prepare_dataset(pcd1,pcd2,voxel_size)


# result= execute_global_registration(source_down, target_down, source_fpfh,target_fpfh, voxel_size)

# print(" transformation is : \n {}".format(result.transformation))


# draw_registration_result(source, target, result.transformation)