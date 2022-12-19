import numpy as np
import ifcopenshell
from ifcopenshell.api import run

O = 0., 0., 0.
X = 1., 0., 0.
Y = 0., 1., 0.
Z = 0., 0., 1.

class Model:
    model = None
    body = None
    storey = None
    
    def __init__(self):
        self.__create_empty_model()

    def __create_empty_model(self):
        # Create a blank model
        self.model = ifcopenshell.file()
        # All projects must have one IFC Project element
        project = run("root.create_entity", self.model, ifc_class="IfcProject", name="My Project")
        # Geometry is optional in IFC, but because we want to use geometry in this example, let's define units
        # Assigning without arguments defaults to metric units
        run("unit.assign_unit", self.model)
        # Let's create a modeling geometry context, so we can store 3D geometry (note: IFC supports 2D too!)
        context = run("context.add_context", self.model, context_type="Model")
        # In particular, in this example we want to store the 3D "body" geometry of objects, i.e. the body shape
        self.body = run(
            "context.add_context", self.model,
            context_type="Model", context_identifier="Body", target_view="MODEL_VIEW", parent=context
        )
        # Create a site, building, and storey. Many hierarchies are possible.
        site = run("root.create_entity", self.model, ifc_class="IfcSite", name="My Site")
        building = run("root.create_entity", self.model, ifc_class="IfcBuilding", name="Building A")
        self.storey = run("root.create_entity", self.model, ifc_class="IfcBuildingStorey", name="Ground Floor")
        # Since the site is our top level location, assign it to the project
        # Then place our building on the site, and our storey in the building
        run("aggregate.assign_object", self.model, relating_object=project, product=site)
        run("aggregate.assign_object", self.model, relating_object=site, product=building)
        run("aggregate.assign_object", self.model, relating_object=building, product=self.storey)

    def create_2pt_wall(self, p1, p2, elevation, height, thickness, container, wall_type=None):
        p1 = np.array([p1[0],p1[1]])
        p2 = np.array([p2[0],p2[1]])

        wall = run("root.create_entity", self.model, ifc_class="IfcWall")
        length = float(np.linalg.norm(p2 - p1))
        representation = run("geometry.add_wall_representation", self.model, context=self.body, length=length, height=height, thickness=thickness)
        v = p2 - p1
        v = np.divide(v,float(np.linalg.norm(v)),casting='unsafe')
        matrix = np.array([
            [v[0], -v[1], 0, p1[0]],
            [v[1], v[0], 0, p1[1]],
            [0, 0, 1, elevation],
            [0, 0, 0, 1],
        ])
        run("geometry.edit_object_placement", self.model, product=wall, matrix=matrix)
        run("geometry.assign_representation", self.model, product=wall, representation=representation)
        run("spatial.assign_container", self.model, relating_structure=container, product=wall)
        if wall_type:
            run("type.assign_type", self.model, related_object=wall, relating_type=wall_type)

        return wall

    def get_model(self):
        return self.model
