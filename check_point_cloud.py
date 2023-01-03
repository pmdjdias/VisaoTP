import open3d as o3d
import sys
import numpy as np



pcd = o3d.io.read_point_cloud(sys.argv[1])

# pcd.paint_uniform_color([1, 0.6, 0.0])

o3d.visualization.draw_geometries([pcd])

# o3d.io.write_point_cloud("pcd_painted.ply", pcd)
