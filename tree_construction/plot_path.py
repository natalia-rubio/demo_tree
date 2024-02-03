import pickle
import numpy as np
import matplotlib.pyplot as plt
import pdb

def load_dict(filename_):
    with open(filename_, 'rb') as f:
        dict = pickle.load(f)
    return dict

paths = load_dict("tree_construction/path")

pdb.set_trace()

plt.clf()
for path in paths:
    x = []
    y = []
    for pt in path:
        x.append(pt[0])
        y.append(pt[1])
    plt.scatter(x, y)
plt.show()