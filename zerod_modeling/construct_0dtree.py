import json 
import numpy as np
import sys
sys.path.append("/Users/natalia/Desktop/demo_tree")
from tools.basic import *

def get_cval_dict(node_data_dict):
    cval_dict = dict()
    mu = 0.04 # poise
    rho = 1.06 # g/cm^3
    cval_dict = dict()

    for i in node_data_dict.keys():
        if i == 0:
            v_name = "aorta_inlet"
            length = 0
        elif i == 1:
            v_name = "aorta_right_outlet"
            length = 0
        elif i == 2:
            v_name = "pulmo_inlet"
            length = np.sqrt(
                (node_data_dict[3]["x"] - node_data_dict[2]["x"])**2 + \
                (node_data_dict[3]["y"] - node_data_dict[2]["y"])**2 + \
                (node_data_dict[3]["z"] - node_data_dict[2]["z"])**2)
        elif i == 3:
            v_name = "pulmo_right_outlet"
            length = 0
        elif i == 4:
            v_name = "pulmo_left_outlet"
            length = 0

        A_nom = node_data_dict[i]["area"]
        radius = np.sqrt(A_nom/np.pi)
        A_sten = A_nom*1.001
        cval_dict.update({i: {"r_poiseuille" : 8*mu*length/(np.pi*(radius**4)),
                                "r_stenosis" : (1.52*rho/(2*A_nom**2))*((A_nom/A_sten) - 1)**2,
                                "inductance" : length*rho/A_nom,
                                "length" : length,
                                "name" : v_name
                                }})
    return cval_dict

def get_input_dict(cval_dict, coef_dict):
    input_dict = {
    "description": {
            "description of test case" : "steady flow -> bifurcation (with R's) -> R",
            "analytical results" : [   "Boundary conditions:",
                                            "inlet:",
                                                "flow rate: Q = 5",
                                            "outlet1:",
                                                "resistance + distal pressure: R1 = 100, Pd1 = 0",
                                            "outlet2:",
                                                "resistance + distal pressure: R2 = 100, Pd2 = 0",
                                            "outlet3:",
                                                "resistance + distal pressure: R2 = 100, Pd2 = 0",

                                        "Solutions:",
                                            "outlet flow1 = Q1 = (Q * (R2 + R_poiseuille2) - Pd1 + Pd2) / (R1 + R_poiseuille1 + R2 + R_poiseuille2) = (5 * (1000 + 500) - 50 + 200) / (100 + 400 + 1000 + 500) = 3.825",
                                            "outlet flow2 = Q2 = (Q * (R1 + R_poiseuille1) - Pd2 + Pd1) / (R1 + R_poiseuille1 + R2 + R_poiseuille2) = (5 * (100 + 400) - 200 + 50 ) / (100 + 400 + 1000 + 500) = 1.175",
                                            "outlet pressure1 = Q1 * R1 + Pd1 =  3.825 * 100  +  50 = 432.5",
                                            "outlet pressure2 = Q2 * R2 + Pd2 =  1.175 * 1000 + 200 = 1375.",
                                            "junction pressure = outlet pressure1 + Q1 * R_poiseuille1 = 432.5 + 3.825 * 400 = 1962.5",
                                            "inlet pressure = junction pressure + Q * R_poiseuille0 = 1962.5 + 5 * 300 = 3462.5"
                                   ]
    },
    "boundary_conditions": [
        {
            "bc_name": "INFLOW",
            "bc_type": "FLOW",
            "bc_values": {
                "Q": [
                    134.2528516821196,
                    134.2528516821196
                ],
                "t": [
                    0.0,
                    1.0
                ]
            }
        },
        {
            "bc_name": "OUT1",
            "bc_type": "RESISTANCE",
            "bc_values": {
                "Pd": 0.0,
                "R": 2500.0
            }
        },
        {
            "bc_name": "OUT2",
            "bc_type": "RESISTANCE",
            "bc_values": {
                "Pd": 0.0,
                "R": 2500.0
            }
        },
        {
            "bc_name": "OUT3",
            "bc_type": "RESISTANCE",
            "bc_values": {
                "Pd": 0.0,
                "R": 2500.0
            }
        }
    ],
    "junctions": [
        {
            "inlet_vessels": [
                0
            ],
            "junction_name": "AORTA_JUNCTION",
            "junction_type": "BloodVesselJunction",
            "outlet_vessels": [
                1,
                2
            ],
            "junction_values": {
                "R_poiseuille": list(-1*coef_dict["Aorta"][1]),
                "L": list(-1*coef_dict["Aorta"][2]),
                #"C": [0,]+list(0*coef_dict["Aorta"][0]),
                "stenosis_coefficient": list(-1*coef_dict["Aorta"][0])
            }
        },
        {
            "inlet_vessels": [
                2
            ],
            "junction_name": "PULMO_JUNCTION",
            "junction_type": "BloodVesselJunction",
            "outlet_vessels": [
                3,
                4
            ],
            "junction_values": {
                "R_poiseuille": list(-1*coef_dict["Pulmo"][1]),
                "L": list(-1*coef_dict["Pulmo"][2]),
                #"C": [0,]+list(0*coef_dict["Pulmo"][0]),
                "stenosis_coefficient": list(-1*coef_dict["Pulmo"][0])
            }
        }
    ],
    "simulation_parameters": {
        "number_of_cardiac_cycles": 2,
        "number_of_time_pts_per_cardiac_cycle": 5
    },
    "vessels": [
        {
            "boundary_conditions": {
                "inlet": "INFLOW"
            },
            "vessel_id": 0,
            "vessel_length": cval_dict[0]["length"],
            "vessel_name": cval_dict[0]["name"],
            "zero_d_element_type": "BloodVessel",
            "zero_d_element_values": {
                "R_poiseuille": cval_dict[0]["r_poiseuille"],
                "L": cval_dict[0]["inductance"],
                "C": 0,
                "stenosis_coefficient": cval_dict[0]["r_stenosis"]
            }
        },
        {
            "boundary_conditions": {
                "outlet": "OUT1"
            },
            "vessel_id": 1,
            "vessel_length": cval_dict[1]["length"],
            "vessel_name": cval_dict[1]["name"],
            "zero_d_element_type": "BloodVessel",
            "zero_d_element_values": {
                "R_poiseuille": cval_dict[1]["r_poiseuille"],
                "L": cval_dict[1]["inductance"],
                "C": 0,
                "stenosis_coefficient": cval_dict[1]["r_stenosis"]
            }
        },
        {
            "boundary_conditions": {
            },
            "vessel_id": 2,
            "vessel_length": cval_dict[2]["length"],
            "vessel_name": cval_dict[2]["name"],
            "zero_d_element_type": "BloodVessel",
            "zero_d_element_values": {
                "R_poiseuille": cval_dict[2]["r_poiseuille"],
                "L": cval_dict[2]["inductance"],
                "C": 0,
                "stenosis_coefficient": cval_dict[2]["r_stenosis"]
            }
        },
                {
            "boundary_conditions": {
                "outlet": "OUT2"
            },
            "vessel_id": 3,
            "vessel_length": cval_dict[3]["length"],
            "vessel_name": cval_dict[3]["name"],
            "zero_d_element_type": "BloodVessel",
            "zero_d_element_values": {
                "R_poiseuille": cval_dict[3]["r_poiseuille"],
                "L": cval_dict[3]["inductance"],
                "C": 0,
                "stenosis_coefficient": cval_dict[3]["r_stenosis"]
            }
        },
                {
            "boundary_conditions": {
                "outlet": "OUT3"
            },
            "vessel_id": 4,
            "vessel_length": cval_dict[4]["length"],
            "vessel_name": cval_dict[4]["name"],
            "zero_d_element_type": "BloodVessel",
            "zero_d_element_values": {
                "R_poiseuille": cval_dict[4]["r_poiseuille"],
                "L": cval_dict[4]["inductance"],
                "C": 0,
                "stenosis_coefficient": cval_dict[4]["r_stenosis"]
            }
        }
    ]
}
    return input_dict

c_val_dict = get_cval_dict(load_dict("synthetic_tree/node_data_dict"))
coef_dict = load_dict("synthetic_tree/coef_dict")
input_dict = get_input_dict(c_val_dict, coef_dict)
print(coef_dict)
with open(f"synthetic_tree/synthetic_tree_0d_input.json", "w") as outfile: 
            json.dump(input_dict, outfile)