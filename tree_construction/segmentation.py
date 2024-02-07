import numpy as np
import sv
import pickle
import pdb
def save_dict(di_, filename_):
    with open(filename_, 'wb') as f:
        pickle.dump(di_, f)

def get_inlet1_segmentations(geo_params):
    num_pts =10
    char_len = 0.5310796510320017*15

    y_in = np.linspace(-char_len/2, 0, num_pts, endpoint = True)
    inlet_path_points_list = [[0.0, float(y), 0.0] for y in y_in]
    inlet_path = sv.pathplanning.Path()
    for point in inlet_path_points_list:
        inlet_path.add_control_point(point)
    inlet_path_points_list = inlet_path.get_control_points()
    inlet_path_curve_points = inlet_path.get_curve_points()

    segmentations = []

    for i in range(num_pts-1):
        contour = sv.segmentation.Circle(radius = geo_params["r1"],
                                    center = inlet_path_points_list[i],
                                    normal = inlet_path.get_curve_tangent(inlet_path_curve_points.index(inlet_path_points_list[i])))
        segmentations.append(contour)

    r_side = geo_params["r1"]
    r_top = (2*geo_params["r1"]+geo_params["r2"])/3
    r_bottom = geo_params["r1"]
    num_el_pts = 20
    contour_pts = []
    y = 0.25#inlet_path_points_list[-1][1]
    for i in range(num_el_pts):
        x = r_side * (1-i /num_el_pts)
        z = r_top * np.sqrt(1 - (x/r_side)**2)
        contour_pts.append([x, y, z])

    for i in range(num_el_pts):
        x = -r_side * (i /num_el_pts)
        z = r_top * np.sqrt(1 - (x/r_side)**2)
        contour_pts.append([x, y, z])

    for i in range(num_el_pts):
        x = -r_side * (1- i /num_el_pts)
        z = -r_top * np.sqrt(1 - (x/r_side)**2)
        contour_pts.append([x, y, z])

    for i in range(num_el_pts):
        x = r_side * (i /num_el_pts)
        z = -r_top * np.sqrt(1 - (x/r_side)**2)
        contour_pts.append([x, y, z])

    contour = sv.segmentation.Contour(contour_pts)
    segmentations.append(contour)
    return inlet_path, segmentations

def get_u1_segmentations(geo_params):
    num_pts = 8#10
    inset = 1
    char_len = 0.5310796510320017*20
    y_in = np.linspace(-char_len, 0, num_pts+1, endpoint = True)

    r = np.linspace(0, char_len, num_pts, endpoint = True)
    theta = np.ones((num_pts,)) * geo_params["angle2"]
    theta = np.pi/2 + np.pi * theta / 180
    outlet1_x = r * np.cos(theta)
    outlet1_y = r * np.sin(theta)
    outlet1_y = outlet1_y 
    outlet1_path_points_list = [[float(outlet1_x[i]), float(outlet1_y[i]), 0.0] for i in range(1, num_pts)]
    outlet1_path_points_list.reverse()

    r = np.linspace(0, char_len, num_pts, endpoint = True)#[2:]
    theta = np.ones((num_pts,)) * geo_params["angle3"]
    theta = np.pi/2 - np.pi * theta / 180
    outlet2_x = r * np.cos(theta) #-  geo_params["inlet_radius"]/2
    outlet2_y = r * np.sin(theta)
    outlet2_y = outlet2_y #- geo_params["inlet_radius"]*1.5
    outlet2_path_points_list = [[float(outlet2_x[i]), float(outlet2_y[i]), 0.0] for i in range(1, num_pts)]

    outlet1_path_points_list.append([0.0, 0.0, 0.0])

    u_path = sv.pathplanning.Path()


    for i, point in enumerate(outlet1_path_points_list):
        if i == 0:
            u_path.add_control_point(point)
        else:
            u_path.add_control_point(point, 0)


    for point in outlet2_path_points_list:
        u_path.add_control_point(point, 0)

    u_path_points_list = u_path.get_control_points()
    u_path_curve_points = u_path.get_curve_points()


    segmentations = []

    for i in range(num_pts-1):
        contour = sv.segmentation.Circle(radius = geo_params["r3"],
                                    center = u_path_points_list[i],
                                    normal = u_path.get_curve_tangent(u_path_curve_points.index(u_path_points_list[i])))
        segmentations.append(contour)

    r_top = geo_params["r1"]*2.2
    r_side = geo_params["r1"]
    #r_side = geo_params["outlet2_radius"]*1.3
    r_bottom = geo_params["r1"]*2
    num_el_pts = 20
    contour_pts = []

    for i in range(num_el_pts):
        z = r_side * (1-i /num_el_pts)
        y = r_top * np.sqrt(1 - (z/r_side)**2)
        contour_pts.append([0, y, z])

    for i in range(num_el_pts):
        z = -r_side * (i /num_el_pts)
        y = r_top * np.sqrt(1 - (z/r_side)**2)
        contour_pts.append([0, y, z])

    for i in range(num_el_pts):
        z = -r_side * (1- i /num_el_pts)
        y = -r_top * np.sqrt(1 - (z/r_side)**2)
        contour_pts.append([0, y, z])

    for i in range(num_el_pts):
        z = r_side * (i /num_el_pts)
        y = -r_top * np.sqrt(1 - (z/r_side)**2)
        contour_pts.append([0, y, z])

    contour = sv.segmentation.Contour(contour_pts)
    segmentations.append(contour)

    for i in range(num_pts, 2*num_pts - 1):
        contour = sv.segmentation.Circle(radius = geo_params["r2"],
                                    center = u_path_points_list[i],
                                    normal = u_path.get_curve_tangent(u_path_curve_points.index(u_path_points_list[i])))
        segmentations.append(contour)

    return u_path, segmentations

def get_inlet2_segmentations(geo_params):
    num_pts = 5

    char_len = geo_params["r2"]
    char_len = 0.23*15
    
    y_in = np.linspace(-3*char_len,0.0*geo_params["r3"], num_pts, endpoint = True)

    up_shift = 3*char_len/2
    inlet_path_points_list_orig = [[0.0, float(y)+up_shift, 0.0] for y in y_in]
    inlet_path_points_list = []
    x_shift = -np.sin(geo_params["angle3"]*np.pi/180)*0.5310796510320017*20
    y_shift = np.cos(geo_params["angle3"]*np.pi/180)*0.5310796510320017*20

    pulmo_in = print("Pulmo inlet = " + str((-np.sin(geo_params['angle3']*np.pi/180)*(up_shift-char_len/2))+x_shift) \
                     + ", " + str((np.cos(geo_params['angle3']*np.pi/180)*(up_shift-char_len/2))+y_shift))
    
    for point in inlet_path_points_list_orig:

        inlet_path_points_list.append([(np.cos(geo_params["angle3"]*np.pi/180)*point[0] - np.sin(geo_params["angle3"]*np.pi/180)*point[1])+x_shift, 
                                       (np.sin(geo_params["angle3"]*np.pi/180)*point[0] + np.cos(geo_params["angle3"]*np.pi/180)*point[1])+y_shift, 
                                       point[2]])
    inlet_path = sv.pathplanning.Path()
    for point in inlet_path_points_list:
        inlet_path.add_control_point(point)
    inlet_path_points_list = inlet_path.get_control_points()
    inlet_path_curve_points = inlet_path.get_curve_points()


    segmentations = []

    for i in range(num_pts):
        contour = sv.segmentation.Circle(radius = geo_params["r3"],
                                    center = inlet_path_points_list[i],
                                    normal = inlet_path.get_curve_tangent(inlet_path_curve_points.index(inlet_path_points_list[i])))
        segmentations.append(contour)

    r_side = (3*geo_params["r3"]+0*geo_params["r4"])/3
    r_top = (3*geo_params["r3"]+0*geo_params["r4"])/3
    r_bottom = geo_params["r3"]
    num_el_pts = 20
    contour_pts = []
    y = 0 #inlet_path_points_list[-1][1] #geo_params["inlet_radius"]#
    for i in range(num_el_pts):
        x = r_side * (1-i /num_el_pts)
        z = r_top * np.sqrt(1 - (x/r_side)**2)
        contour_pts.append([x, y, z])

    for i in range(num_el_pts):
        x = -r_side * (i /num_el_pts)
        z = r_top * np.sqrt(1 - (x/r_side)**2)
        contour_pts.append([x, y, z])

    for i in range(num_el_pts):
        x = -r_side * (1- i /num_el_pts)
        z = -r_top * np.sqrt(1 - (x/r_side)**2)
        contour_pts.append([x, y, z])

    for i in range(num_el_pts):
        x = r_side * (i /num_el_pts)
        z = -r_top * np.sqrt(1 - (x/r_side)**2)
        contour_pts.append([x, y, z])

    contour = sv.segmentation.Contour(contour_pts)
    #segmentations.append(contour)
    return inlet_path, segmentations

def get_u2_segmentations(geo_params):
    print(geo_params)
    num_pts = 2*4#10
    inset = 1
    #char_len = geo_params["inlet_radius"]*12
    char_len = 0.23*20*2
    up_shift = 3*0.23*15/2
    #y_in = np.linspace(-char_len, 0, num_pts+1, endpoint = True)


    r = np.linspace(0, char_len, num_pts, endpoint = True)#[2:]
    theta = np.ones((num_pts,)) * geo_params["angle4"]
    theta = np.pi/2 + np.pi * theta / 180
    outlet1_x = r * np.cos(theta) #+  geo_params["inlet_radius"]/2
    outlet1_y = r * np.sin(theta)
    outlet1_y = outlet1_y #-  geo_params["inlet_radius"]*1.5
    outlet1_path_points_list_orig = [[float(outlet1_x[i]), float(outlet1_y[i]) + up_shift, 0.0] for i in range(1, num_pts)]
    outlet1_path_points_list_orig.reverse()


    theta = np.ones((num_pts,)) * geo_params["angle5"]
    theta = np.pi/2 - np.pi * theta / 180
    outlet2_x = r * np.cos(theta) #-  geo_params["inlet_radius"]/2
    outlet2_y = r * np.sin(theta)
    outlet2_y = outlet2_y #- geo_params["inlet_radius"]*1.5
    outlet2_path_points_list_orig = [[float(outlet2_x[i]), float(outlet2_y[i]) + up_shift, 0.0] for i in range(1, num_pts)]

    outlet1_path_points_list_orig.append([0.0, up_shift, 0.0])
    outlet1_path_points_list = []
    x_shift = -np.sin(geo_params["angle3"]*np.pi/180)*0.5310796510320017*20
    y_shift = np.cos(geo_params["angle3"]*np.pi/180)*0.5310796510320017*20
    for point in outlet1_path_points_list_orig:

        outlet1_path_points_list.append([(np.cos(geo_params["angle3"]*np.pi/180)*point[0] \
                                          - np.sin(geo_params["angle3"]*np.pi/180)*point[1])+x_shift, 
                                       (np.sin(geo_params["angle3"]*np.pi/180)*point[0] + 
                                        np.cos(geo_params["angle3"]*np.pi/180)*point[1])+y_shift, 
                                       point[2]])


    outlet2_path_points_list = []
    for point in outlet2_path_points_list_orig:

        outlet2_path_points_list.append([(np.cos(geo_params["angle3"]*np.pi/180)*point[0] \
                                          - np.sin(geo_params["angle3"]*np.pi/180)*point[1])+x_shift, 
                                       (np.sin(geo_params["angle3"]*np.pi/180)*point[0] \
                                        + np.cos(geo_params["angle3"]*np.pi/180)*point[1])+y_shift, 
                                       point[2]])
        
    u_path = sv.pathplanning.Path()


    for i, point in enumerate(outlet1_path_points_list):
        if i == 0:
            u_path.add_control_point(point)
        else:
            u_path.add_control_point(point, 0)


    for point in outlet2_path_points_list:
        try:
            u_path.add_control_point(point, 0)
        except:
    
            continue
        
    u_path_points_list = u_path.get_control_points()
    u_path_curve_points = u_path.get_curve_points()


    segmentations = []

    for i in range(num_pts-1):
        contour = sv.segmentation.Circle(radius = geo_params["r5"], #geo_params["outlet2_radius"],
                                    center = u_path_points_list[i],
                                    normal = u_path.get_curve_tangent(u_path_curve_points.index(u_path_points_list[i])))
        segmentations.append(contour)

    r_top = geo_params["r3"]*2.2+ geo_params["r4"]
    r_side = geo_params["r3"]
    #r_side = geo_params["outlet2_radius"]*1.3
    r_bottom = geo_params["r3"]*2
    num_el_pts = 20
    contour_pts = []

    y_plus = 0# geo_params["inlet_radius"]/3
    for i in range(num_el_pts):
        z = r_side * (1-i /num_el_pts)
        y = r_top * np.sqrt(1 - (z/r_side)**2)
        contour_pts.append([-np.sin(geo_params["angle3"]*np.pi/180)*(y + up_shift) + x_shift, 
                           np.cos(geo_params["angle3"]*np.pi/180) * (y + up_shift) + y_shift, z])

    for i in range(num_el_pts):
        z = -r_side * (i /num_el_pts)
        y = r_top * np.sqrt(1 - (z/r_side)**2)
        contour_pts.append([-np.sin(geo_params["angle3"]*np.pi/180)*(y + up_shift) + x_shift, 
                            np.cos(geo_params["angle3"]*np.pi/180) * (y + up_shift) + y_shift, z])

    for i in range(num_el_pts):
        z = -r_side * (1- i /num_el_pts)
        y = -r_top * np.sqrt(1 - (z/r_side)**2)
        contour_pts.append([-np.sin(geo_params["angle3"]*np.pi/180)*(y + up_shift) + x_shift,
                            np.cos(geo_params["angle3"]*np.pi/180) * (y + up_shift) + y_shift, z])

    for i in range(num_el_pts):
        z = r_side * (i /num_el_pts)
        y = -r_top * np.sqrt(1 - (z/r_side)**2)
        contour_pts.append([-np.sin(geo_params["angle3"]*np.pi/180)*(y + up_shift) + x_shift, 
                            np.cos(geo_params["angle3"]*np.pi/180) * (y + up_shift) + y_shift, z])

    contour = sv.segmentation.Contour(contour_pts)
    segmentations.append(contour)

    for i in range(num_pts, 2*num_pts - 1):
        contour = sv.segmentation.Circle(radius = geo_params["r4"], #geo_params["outlet1_radius"],
                                    center = u_path_points_list[i],
                                    normal = u_path.get_curve_tangent(u_path_curve_points.index(u_path_points_list[i])))
        segmentations.append(contour)

    return u_path, segmentations

def save_path(paths):
    total_path_list = []

    for path in paths:
        total_path_list += [path.get_control_points(),]
    save_dict(total_path_list, "tree_construction/path")

def get_tree_segmentation(geo_params):
    inlet1_path, inlet1_segmentations = get_inlet1_segmentations(geo_params)
    inlet1_segmentations_polydata_objects = [contour.get_polydata() for contour in inlet1_segmentations]

    u1_path, u1_segmentations = get_u1_segmentations(geo_params)
    u1_segmentations_polydata_objects = [contour.get_polydata() for contour in u1_segmentations]

    inlet2_path, inlet2_segmentations = get_inlet2_segmentations(geo_params)
    inlet2_segmentations_polydata_objects = [contour.get_polydata() for contour in inlet2_segmentations]

    u2_path, u2_segmentations = get_u2_segmentations(geo_params)
    u2_segmentations_polydata_objects = [contour.get_polydata() for contour in u2_segmentations]

    save_path([inlet1_path, u1_path, inlet2_path, u2_path])
    return inlet1_segmentations_polydata_objects, u1_segmentations_polydata_objects, inlet2_segmentations_polydata_objects, u2_segmentations_polydata_objects
