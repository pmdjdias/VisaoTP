
import numpy as np
import open3d as o3d
import argparse




def main():
    # using argparse to create UI
    parser= argparse.ArgumentParser(description='Select voxel size and a name file to resize the original point cloud ')

    parser.add_argument("-v", "--voxel_size" ,type=int,default=0.05, help= "Using time mode will end the test with a duration, in seconds, equal to the value of -mv or --max_value.")
    parser.add_argument("-n ", "--name_file", type=str, help= "name of the file you")

    args = parser.parse_args()
    

    if  args.voxel_size == None or args.name_file == None:
        print("no arguments added, please use 'python3 reconstruction_Vsize_down.py -h' or --help to see the arguments") 
        quit()

    print("Loading point cloud \n ...")
    
    pcd1= o3d.io.read_point_cloud(args.name_file)

    
    print("donwsampling point cloud ")
    # o3d.geometry.voxel_down_sample(pcd1,args.voxel_size)    
    pcd1.voxel_down_sample(voxel_size=args.voxel_size)
    # convertionOfPlyToPcd("/home/jose/Documents/UA/VisaoTP/point_cloud_classroom(original)/sala119.ply","/home/jose/Documents/.pcd")

    newname= "filtered_"+args.name_file
    o3d.io.write_point_cloud(newname, pcd1)
    


# def convertionOfPlyToPcd(ply_file,pcd_file):
#     input_file = open(ply_file)
#     out= pcd_file   
#     output = open(out, 'w')
#     write_points = False
#     points_counter = 0
#     nr_points = 0
#     for s in input_file.readlines():
#         if s.find("element vertex") != -1:
#             nr_points = int(s.split(" ")[2].rstrip().lstrip())
#             new_header = header.replace("XXXX", str(nr_points))
#             output.write(new_header)
#             output.write("\n")
#         if s.find("end_header") != -1:
#             write_points = True
#             continue
#         if write_points and points_counter < nr_points:
#             points_counter = points_counter + 1
#             output.write(" ".join(s.split(" ", 4)[:4]))
#             output.write("\n")
#     input_file.close()
#     output.close()


if __name__ =="__main__":
    
    main()
