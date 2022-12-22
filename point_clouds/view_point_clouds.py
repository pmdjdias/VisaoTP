#! /usr/bin/env python3



import numpy as np
import open3d as o3d
import argparse

def main():
    # parser= argparse.ArgumentParser(description='reads point cloud from a file. ')

    # parser.add_argument("-f", "--file" ,type=str, help= "add the file name.")
    # parser.add_argument("-c ", "--color", type=bool,default=False, help= "true or false, normally false, if true changes the color to orange.")

    # args = parser.parse_args()
    # #color of the point cloud
    # if args.color:
    #     pcd1.paint_uniform_color([0, 0.6, 0.0])
    

    #reads the point cloud from a file
    # pcd1= o3d.io.read_point_cloud(args.file)

    pcd1=o3d.io.read_point_cloud("point_clouds/point_clouds_todas/cloud_12-21-2022 17-50-15.ply")
    


    o3d.visualization.draw_geometries([pcd1],
			front=[ 0.23614134979016571, 0.128116079769134, -0.9632359695442585 ],
			lookat= [ -0.45768684148788452, -0.34095668792724609, 1.6455000638961792 ],
			up=[ -0.12323811424252881, -0.97931741385638282, -0.16046734906388865 ],
			zoom = 0.71999999999999997)
		




if __name__ == "__main__":
    main()
