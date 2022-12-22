
import numpy as np
import open3d as o3d
import argparse




def main():
    # using argparse to create UI
    parser= argparse.ArgumentParser(description='Select voxel size and a name file to resize the original point cloud ')

    parser.add_argument("-v", "--voxel_size" ,type=int,default=0.012, help= "Using time mode will end the test with a duration, in seconds, equal to the value of -mv or --max_value.")
    parser.add_argument("-n ", "--name_file", type=str, help= "name of the file you")

    args = parser.parse_args()
    

    if  args.voxel_size == None or args.name_file == None:
        print("no arguments added, please use 'python3 reconstruction_Vsize_down.py -h' or --help to see the arguments") 
        quit()

    print("Loading point cloud \n ...")
    
    pcd1= o3d.io.read_point_cloud(args.name_file)

    
    print("donwsampling point cloud ")
    pcd1_down = pcd1.voxel_down_sample(voxel_size=args.voxel_size)  

    newname= "filtered_fullroom1.ply"
    print("saving  \n ...")
    o3d.io.write_point_cloud(newname, pcd1_down)



if __name__ =="__main__":
    
    main()
