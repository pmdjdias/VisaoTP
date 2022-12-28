import open3d as o3d 
import numpy as np
import copy
import sys

   
if len(sys.argv) >= 1:
    for i in range(1, len(sys.argv)):
        point_cloud=sys.argv[i]
        print("cleaning point cloud: "+point_cloud)

        print("\n --------------------------\n")
        #import point cloud in sys.argv[1] and clean the point cloud
        pcd = o3d.io.read_point_cloud(point_cloud)
        print("point cloud before cleaning")
        
        # o3d.visualization.draw_geometries([pcd])
        
        pcd = pcd.voxel_down_sample(voxel_size=0.012)
        pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=25))
        pcd.orient_normals_towards_camera_location(camera_location=np.array([0, 0, 0]))
        print("point cloud after cleaning")
        
        # o3d.visualization.draw_geometries([pcd])
        print("saving")
        #save the point cloud with the same name as sys.argv[1]  
        o3d.io.write_point_cloud(point_cloud, pcd)
else:
    print("Please specify one or more point clouds to clean")

