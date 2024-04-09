import sys
import vtk
import os
import numpy as np
import pdb
sys.path.append("/Users/natalia/Desktop/demo_tree")
from vtk.util.numpy_support import vtk_to_numpy as v2n
from tqdm import tqdm
from tools.basic import *
from tools.get_bc_integrals import get_res_names
#from util.junction_proc import *
from geo_processing import *
from tools.vtk_functions import read_geo, write_geo, calculator, cut_plane, connectivity, get_points_cells, clean, Integration
import pickle
from sklearn.linear_model import LinearRegression

def sort_result(sol_path1d, only_caps=False, num_time_steps = 1000):
    """
    Get all result array names
    Args:
        inp: vtk InputConnection
        names: list of names to search for
    Returns:
        list of result array names
    """
    soln = read_geo(sol_path1d).GetOutput()
    soln_array = get_all_arrays(soln)
    points = v2n(soln.GetPoints().GetData())
    res_names = list(soln_array.keys())
    res_names.sort()

    pt_id = soln_array["GlobalNodeId"].astype(int)
    branch_id = soln_array["BranchIdTmp"].astype(int)
    junction_id = soln_array["BifurcationId"].astype(int)

    branch_soln_dict = dict()

    for i in range(np.max(branch_id)+1):
        
        branch_pts = np.where(branch_id == i)
        ordered_inds = np.argsort(pt_id[branch_pts])
        locs = (points[branch_pts])[ordered_inds]
        dist = np.asarray([0,] + list(np.cumsum(np.linalg.norm(locs[1:,:] - locs[:-1,:], axis = 1))))

        branch_dict = {"x": locs[:,0],
                       "y": locs[:,1],
                       "z": locs[:,2],
                       "dist": dist,
                       "pressure": soln_array[f"pressure_{format(int(num_time_steps), '05d')}"][branch_pts][ordered_inds],
                       "flow": soln_array[f"velocity_{format(int(num_time_steps), '05d')}"][branch_pts][ordered_inds]}
        
        branch_soln_dict.update({i : branch_dict})
    
    save_dict(branch_soln_dict, "synthetic_tree/branch_soln_dict")
    return branch_soln_dict

def get_node_data(sol_path1d, only_caps=False, num_time_steps = 1000):
    soln = read_geo(sol_path1d).GetOutput()
    soln_array = get_all_arrays(soln)
    points = v2n(soln.GetPoints().GetData())
    res_names = list(soln_array.keys())
    res_names.sort()

    pt_id = soln_array["GlobalNodeId"].astype(int)
    branch_id = soln_array["BranchIdTmp"].astype(int)
    junction_id = soln_array["BifurcationId"].astype(int)

    point_list = ["aorta_inlet", "aorta_right_outlet", "aorta_left_outlet", "pulmo_inlet", "pulmo_right_outlet", "pulmo_left_outlet"]
    # points_of_interest = np.asarray([[0, 3.633, -3.633, -4.813, -5.724, -8.107],
    #         [-3.983, 9.981, 9.981, 13.223, 19.433, 18.565],
    #         [0,0,0,0,0,0]]).T
    points_of_interest = np.asarray([[0, 3.633, -3.633, -3.633, -4.544, -6.927],
            [-3.983, 9.981, 9.981, 9.981, 16.191, 15.323],
            [0,0,0,0,0,0]]).T
    node_data_dict = dict()
    for i in range(len(point_list)):
        #pdb.set_trace()
        point_ind = pt_id[np.argmin(np.linalg.norm(points - points_of_interest[i,:], axis = 1))]
        branch_id_curr = branch_id[point_ind]

        branch_pts = np.where(branch_id == branch_id_curr)
        ordered_inds = np.argsort(pt_id[branch_pts])
        ordered_pts = pt_id[branch_pts][ordered_inds]
        ordered_point_ind = np.where(ordered_pts == point_ind)[0][0]
        locs = (points[branch_pts])[ordered_inds]
        
        #pdb.set_trace()
        if "inlet" in point_list[i]:
            dist_to_bif = np.sum(np.linalg.norm(locs[ordered_point_ind+1:,:] - locs[ordered_point_ind:-1,:], axis = 1))

        elif "outlet" in point_list[i]:
            dist_to_bif = np.sum(np.linalg.norm(locs[1:ordered_point_ind,:] - locs[0:ordered_point_ind-1,:], axis = 1))
        


        node_data_dict.update({i             : {"index" : point_ind,
                                                "name"  : point_list[i],
                                                "gid"   : pt_id[point_ind],
                                                "x"     : points[point_ind, 0],
                                                "y"     : points[point_ind, 1],
                                                "z"     : points[point_ind, 2],
                                                "pressure" : soln_array[f"pressure_{format(int(num_time_steps), '05d')}"][point_ind],
                                                "flow"     : soln_array[f"velocity_{format(int(num_time_steps), '05d')}"][point_ind],
                                                "area"     : soln_array[f"area"][point_ind],
                                                "dist_to_bif" : dist_to_bif}})
    print(node_data_dict)    
    save_dict(node_data_dict, "synthetic_tree/node_data_dict")
    return

def plot_geometry():
    branch_soln_dict = load_dict("synthetic_tree/branch_soln_dict")
    plt.clf()
    plt.axis('equal')
    for i in range(len(branch_soln_dict.keys())):
        plt.scatter(branch_soln_dict[i]["x"], branch_soln_dict[i]["y"], s = 10, label = f"Branch {i}")
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("y")

    points = [[0, 3.633, -3.633, -4.813,-5.724, -8.107],
              [-3.983, 9.981, 9.981, 13.223, 19.433, 18.565]]
    scatter = plt.scatter(points[0], points[1], s = 50, c = "k", label = "Junctions")
    plt.savefig("results/branch_geometry.png")
    return

def plot_pressure():
    branch_soln_dict = load_dict("synthetic_tree/branch_soln_dict")
    plt.clf()
    for i in range(len(branch_soln_dict.keys())):
        if i == 0:
            shift = 0
        elif i == 1 or i == 2:
            shift = branch_soln_dict[0]["dist"][-1]
        elif i == 3 or i == 4:
            shift = branch_soln_dict[2]["dist"][-1] + branch_soln_dict[0]["dist"][-1]

        plt.plot(branch_soln_dict[i]["dist"]+shift, branch_soln_dict[i]["pressure"]/1333, label = f"Branch {i}")
    plt.legend()
    plt.xlabel("Centerline distance (cm)")
    plt.ylabel("Pressure (mmHg)")
    plt.savefig("results/pressure_over_branches.png")
    return

get_node_data("synthetic_tree/centerline_sol.vtp")
sort_result("synthetic_tree/centerline_sol.vtp")
plot_geometry()
plot_pressure()