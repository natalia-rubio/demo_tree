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
from sim_results_processing.sort_results import *

zerod_baseline_res = np.genfromtxt("synthetic_tree/baseline_0d_results.csv", delimiter = ",")
zerod_baseline_res_dict = dict()
for i in range(7):
    zerod_baseline_res_dict.update({i: {"name": zerod_baseline_res[5+5*i,0], 
                                     "pressure_in": zerod_baseline_res[5+5*i,4],
                                     "pressure_out": zerod_baseline_res[5+5*i,5]}})
zerod_baseline_res_dict[2]["pressure_in"]  = zerod_baseline_res_dict[0]["pressure_in"]

zerod_model_res = np.genfromtxt("synthetic_tree/junction_model_0d_results.csv", delimiter = ",")
zerod_model_res_dict = dict()
for i in range(5):
    zerod_model_res_dict.update({i: {"name": zerod_model_res[5+5*i,0], 
                                     "pressure_in": zerod_model_res[5+5*i,4],
                                     "pressure_out": zerod_model_res[5+5*i,5]}})

branch_soln_dict = load_dict("synthetic_tree/branch_soln_dict")
node_soln_dict = load_dict("synthetic_tree/node_data_dict")

colors1 = ["b", "orange", "g", "r", "m"]
colors2 = ["b", "orange", "g", "g", "r", "m"]
plt.clf()
plt.gcf().set_size_inches(8, 3)
for i in range(len(branch_soln_dict.keys())):
    if i == 0:
        shift = 0
        pt_loc = 0
    elif i == 1 or i == 2:
        shift = branch_soln_dict[0]["dist"][-1]

    elif i == 3 or i == 4:
        shift = branch_soln_dict[2]["dist"][-1] + branch_soln_dict[0]["dist"][-1]
    
    plt.plot(branch_soln_dict[i]["dist"]+shift, branch_soln_dict[i]["pressure"]/1333, color = colors1[i], label = f"Branch {i}")
    plt.scatter(branch_soln_dict[i]["dist"][0]+shift, zerod_baseline_res_dict[i+2]["pressure_in"]/1333, marker = "o", s = 100, facecolors='none', edgecolors = colors1[i])
    plt.scatter(branch_soln_dict[i]["dist"][-1]+shift, zerod_baseline_res_dict[i+2]["pressure_out"]/1333, marker = "s", s = 100, facecolors='none', edgecolors= colors1[i])
for i in range(len(zerod_model_res_dict.keys())):
    junc1_shift = branch_soln_dict[0]["dist"][-1]
    junc2_shift = branch_soln_dict[2]["dist"][-1] + branch_soln_dict[0]["dist"][-1]
    if i == 0:
        pt1_loc = 0
        pt2_loc = 0
    if i == 1:
        pt1_loc = junc1_shift + node_soln_dict[1]["dist_to_bif"]
        pt2_loc = junc1_shift + node_soln_dict[1]["dist_to_bif"]
    if i == 2:
        pt1_loc = junc1_shift + node_soln_dict[2]["dist_to_bif"]
        pt2_loc = junc2_shift - node_soln_dict[3]["dist_to_bif"]
    if i == 3:
        pt1_loc = junc2_shift + node_soln_dict[4]["dist_to_bif"]
        pt2_loc = junc2_shift + node_soln_dict[4]["dist_to_bif"]
    if i == 4:
        pt1_loc = junc2_shift + node_soln_dict[5]["dist_to_bif"]
        pt2_loc = junc2_shift + node_soln_dict[5]["dist_to_bif"]
            
    plt.scatter(pt1_loc, zerod_model_res_dict[i]["pressure_in"]/1333, marker = "*", s = 170, color = colors1[i])
    plt.scatter(pt2_loc, zerod_model_res_dict[i]["pressure_out"]/1333, marker = "*", s = 170, color = colors1[i]) 
pdb.set_trace()
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.xlabel("Centerline distance (cm)")
plt.ylabel("Pressure (mmHg)")
plt.savefig("results/pressure_over_branches_zerod.pdf", bbox_inches='tight')
