#! /usr/bin/env python3



import numpy as np
import open3d as o3d
import argparse

def main():
    parser= argparse.ArgumentParser(description='reads point cloud from a file. ')

    parser.add_argument("-f", "--file" ,type=str, help= "add the file name.")
    parser.add_argument("-c ", "--color", type=bool,default=False, help= "true or false, normally false, if true changes the color to orange.")

    args = parser.parse_args()
    

    #reads the point cloud from a file
    pcd1= o3d.io.read_point_cloud(args.file)

    #color of the point cloud
    if args.color:
        pcd1.paint_uniform_color([0, 0.6, 0.0])

    


    o3d.visualization.draw_geometries([pcd1], zoom=0.3412,
                                    front=[0.4257, -0.2125, -0.8795],
                                    lookat=[2.6172, 2.0475, 1.532],
                                    up=[-0.0694, -0.9768, 0.2024])






    #the 3d view of the result
    o3d.visualization.draw_geometries([pcd1])



if __name__ == "__main__":
    main()
