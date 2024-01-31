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

def sort_result(sol_path1d, only_caps=False, num_time_steps = 800):
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
    num_time_steps = 800
    for i in range(np.max(branch_id)+1):
        
        branch_pts = np.where(branch_id == i)
        ordered_inds = np.argsort(pt_id[branch_pts])
        locs = (points[branch_pts])[ordered_inds]
        #dist = 

        branch_dict = {"x": locs[:,0],
                       "y": locs[:,1],
                       "z": locs[:,2],
                       "pressure": soln_array[f"pressure_00{num_time_steps}"][branch_pts][ordered_inds],
                       "flow": soln_array[f"pressure_00{num_time_steps}"][branch_pts][ordered_inds]}
        
        branch_soln_dict.update({i : branch_dict})
    save_dict(branch_soln_dict, "synthetic_tree/branch_soln_dict")
    return branch_soln_dict

def plot_geometry():
    branch_soln_dict = load_dict("synthetic_tree/branch_soln_dict")
    plt.clf()
    plt.axis('equal')
    for i in range(len(branch_soln_dict.keys())):
        plt.scatter(branch_soln_dict[i]["x"], branch_soln_dict[i]["y"], s = 10, label = f"Branch {i}")
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.savefig("results/branch_geometry.png")
    return

def plot_pressure():
    branch_soln_dict = load_dict("synthetic_tree/branch_soln_dict")
    plt.clf()
    for i in range(len(branch_soln_dict.keys())):
        plt.scatter(branch_soln_dict[i]["x"], branch_soln_dict[i]["y"], s = 10, label = f"Branch {i}")
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.savefig("results/branch_geometry.png")
    return
sort_result("synthetic_tree/centerline_sol.vtp")
plot_geometry()