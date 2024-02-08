'''Test the ROM simulation class. 

   Generate a reduced-order modeling (ROM) simulation input file.

   Use the centerlines and faces from the Demo project.
'''
import os
from pathlib import Path
import sv
import sys
import vtk

## Set some directory paths. 
script_path = "synthetic_tree"
#parent_path = Path(os.path.realpath(__file__)).parent.parent
#data_path = parent_path / 'data'

## Create a ROM simulation.
input_dir = str(script_path + "/" + "input")
rom_simulation = sv.simulation.ROM() 

## Create ROM simulation parameters.
params = sv.simulation.ROMParameters()

## Mesh parameters.
mesh_params = params.MeshParameters()

## Model parameters.
model_params = params.ModelParameters()
model_params.name = "synthetic_tree"
model_params.inlet_face_names = ['cap_2' ] 
model_params.outlet_face_names = ['cap_3', 'cap_37', 'cap_38'] 
model_params.centerlines_file_name = 'synthetic_tree/centerlines/centerline.vtp' 

## Fluid properties.
fluid_props = params.FluidProperties()

## Set wall properties.
#
print("Set wall properties ...")
material = params.WallProperties.OlufsenMaterial()
print("Material model: {0:s}".format(str(material)))

## Set boundary conditions.
#
bcs = params.BoundaryConditions()
#bcs.add_resistance(face_name='outlet', resistance=1333)
bcs.add_velocities(face_name='cap_2', file_name='synthetic_tree/inflow.flow')
bcs.add_resistance(face_name='cap_3', resistance=100.0)
bcs.add_resistance(face_name='cap_37', resistance=0.0)
bcs.add_resistance(face_name='cap_38', resistance=0.0)

## Set solution parameters. 
#
solution_params = params.Solution()
solution_params.time_step = 0.2
solution_params.num_time_steps = 5

## Write a 1D solver input file.
#
output_dir = str("synthetic_tree" + "/" + "baseline_input_files")
rom_simulation.write_input_file(model_order=0, model=model_params, mesh=mesh_params, fluid=fluid_props, material=material, boundary_conditions=bcs, solution=solution_params, directory=output_dir)

## Run a simulation.
#
#fluid_simulation.run(parameters=fluid_params, use_mpi=True, num_processes=4)


