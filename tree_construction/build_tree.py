import sys
sys.path.append("/Users/natalia/Desktop/demo_tree")
#from util.tools.basic import *

from tree_construction.segmentation import *
from tree_construction.modeling_and_meshing import *
import pickle
def load_dict(filename_):
    with open(filename_, 'rb') as f:
        dict = pickle.load(f)
    return dict

geo_name = "tree"
anatomy = "tree"
mesh_divs = 3
geo_params = dict({"r1" : 0.5,
              "r2" : 0.3,
              "r3" : 0.3,
              "r4" : 0.2,
              "r5" : 0.2,
              "angle2" : 20,
              "angle3" : 20,
              "angle4" : 16,
              "angle5" : 16})
segmentations = get_tree_segmentation(geo_params)
print("Segmentation Done!")
model = construct_model(geo_name, segmentations, geo_params)
print("Model Done!")
mesh = get_mesh(geo_name, model, geo_params, anatomy, mesh_divs)
print("Mesh Done!")
