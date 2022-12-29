
# examples/python/Advanced/interactive_visualization.py

import numpy as np
import copy
import open3d as o3d
import sys
import datetime



def clean_point_cloud(point_cloud):
    
    #import point cloud in sys.argv[1] and clean the point cloud
    pcd = o3d.io.read_point_cloud(point_cloud)
    print("point cloud before cleaning")
    o3d.visualization.draw_geometries([pcd])
    pcd = pcd.voxel_down_sample(voxel_size=0.012)
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=25))
    pcd.orient_normals_towards_camera_location(camera_location=np.array([0, 0, 0]))
    print("point cloud after cleaning")
    o3d.visualization.draw_geometries([pcd])

    return pcd



def demo_crop_geometry():
    print("------------------------------------")
    print("Demo for manual geometry cropping ")
    print("------------------------------------ \n")
    print("1) Press 'Y' twice to align geometry with negative direction of y-axis")
    print("2) Press 'K' to lock screen and to switch to selection mode")
    print("3) Drag for rectangle selection,")
    print("   or use ctrl + left click for polygon selection")
    print("4) Press 'C' to get a selected geometry and to save it")
    print("5) Press 'F' to switch to freeview mode")

    #FIXME: nao sei se é preciso mostrar o original
    # print("showing the otiginal point cloud")
    # pcd = o3d.io.read_point_cloud(sys.argv[1])
    # o3d.visualization.draw_geometries_with_editing([pcd])


def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    # source_temp.paint_uniform_color([1, 0.706, 0])
    # target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp])


def pick_points(pcd):
    print("")
    print("1) Please pick at least three correspondences using [shift + left click]")
    print("   Press [shift + right click] to undo point picking")
    print("2) After picking points, press 'Q' to close the window")
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window()
    vis.add_geometry(pcd)
    vis.run()  # user picks points
    vis.destroy_window()
    print("")
    return vis.get_picked_points()


def demo_manual_registration():
    print("manual ICP")
    source = o3d.io.read_point_cloud(sys.argv[1])
    target = o3d.io.read_point_cloud(sys.argv[2])
    print ("\n")
    
    print("Visualization of two point clouds before manual alignment")
    draw_registration_result(source, target, np.identity(4))

    # pick points from two point clouds and builds correspondences
    picked_id_source = pick_points(source)
    picked_id_target = pick_points(target)
    assert (len(picked_id_source) >= 3 and len(picked_id_target) >= 3)
    # ,f"More than 3 points werent chosen, got: {len(picked_id_source)} points picked on the source and {len(picked_id_target)} points picked on the target")
    
    assert (len(picked_id_source) == len(picked_id_target))
    # ,f"Number of points picked on the source and target are different, got:{len(picked_id_source)} points picked on the source and {len(picked_id_target)} points picked on the target")
    corr = np.zeros((len(picked_id_source), 2))
    corr[:, 0] = picked_id_source
    corr[:, 1] = picked_id_target

    # estimate rough transformation using correspondences
    print("computing initial alignment using the corresponding points")
    p2p = o3d.pipelines.registration.TransformationEstimationPointToPoint()
    trans_init = p2p.compute_transformation(source, target,
                                            o3d.utility.Vector2iVector(corr))

    # point-to-point ICP for refinement
    print("Perform point-to-point ICP refinement")
    threshold = 0.03  # 3cm distance threshold
    reg_p2p = o3d.pipelines.registration.registration_icp(
        source, target, threshold, trans_init,
        o3d.pipelines.registration.TransformationEstimationPointToPoint())
    draw_registration_result(source, target, reg_p2p.transformation)
    print(" final icp transformation  computed ")
    print("do you wish to save this transformation? (y/n)")
    save = input()
    if save == 'y':
        print("saving transformation to file")
        # transforming the target using the reg_p2p transformation
        source_transf= source.transform(reg_p2p.transformation)
        newpointcloud=target+source_transf

        #   writing the point cloud name as the current date and time
        now = datetime.datetime.now()
        now = now.strftime("%H-%M_%S")
        filename="finished_cloud_point-"+now+".ply"

        #use clean_point_cloud to clean the point cloud
        newpointcloud =clean_point_cloud(newpointcloud)
        o3d.io.write_point_cloud(filename, newpointcloud)
        o3d.visualization.draw_geometries([newpointcloud])
    else:
        print("not saving transformation to file")
        pass    




if __name__ == "__main__":
    demo_crop_geometry()
    demo_manual_registration()
