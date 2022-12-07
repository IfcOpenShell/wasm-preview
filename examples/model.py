import numpy as np
import ifcopenshell
from ifcopenshell.api import run
import random
import uuid

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


    # Creates an IfcAxis2Placement3D from Location, Axis and RefDirection specified as Python tuples
    # def create_ifcaxis2placement(self, ifcfile, point=O, dir1=Z, dir2=X):
    #     point = ifcfile.createIfcCartesianPoint(point)
    #     dir1 = ifcfile.createIfcDirection(dir1)
    #     dir2 = ifcfile.createIfcDirection(dir2)
    #     axis2placement = ifcfile.createIfcAxis2Placement3D(point, dir1, dir2)
    #     return axis2placement

    # Creates an IfcLocalPlacement from Location, Axis and RefDirection, specified as Python tuples, and relative placement
    # def create_ifclocalplacement(self, ifcfile, point=O, dir1=Z, dir2=X, relative_to=None):
    #     axis2placement = self.create_ifcaxis2placement(ifcfile,point,dir1,dir2)
    #     ifclocalplacement2 = ifcfile.createIfcLocalPlacement(relative_to,axis2placement)
    #     return ifclocalplacement2

    # Creates an IfcPolyLine from a list of points, specified as Python tuples
    # def create_ifcpolyline(self, ifcfile, point_list):
    #     ifcpts = []
    #     for point in point_list:
    #         point = ifcfile.createIfcCartesianPoint(point)
    #         ifcpts.append(point)
    #     polyline = ifcfile.createIfcPolyLine(ifcpts)
    #     return polyline

    # Creates an IfcExtrudedAreaSolid from a list of points, specified as Python tuples
    # def create_ifcextrudedareasolid(self, ifcfile, point_list, ifcaxis2placement, extrude_dir, extrusion):
    #     polyline = self.create_ifcpolyline(ifcfile, point_list)
    #     ifcclosedprofile = ifcfile.createIfcArbitraryClosedProfileDef("AREA", None, polyline)
    #     ifcdir = ifcfile.createIfcDirection(extrude_dir)
    #     ifcextrudedareasolid = ifcfile.createIfcExtrudedAreaSolid(ifcclosedprofile, ifcaxis2placement, ifcdir, extrusion)
    #     return ifcextrudedareasolid

    # def create_wall(self):
    #     wall_length = random.randrange(50)
    #     wall_height = random.randrange(20)
    #     wall_thickness = 0.2

    #     # Let's create a new wall
    #     wall = run("root.create_entity", self.model, ifc_class="IfcWall")
        
    #     storey_placement = self.model.by_type('IfcBuildingStorey')[0].ObjectPlacement
    #     wall_placement = self.create_ifclocalplacement(self.model, relative_to=storey_placement)
    #     print("Wall placement: \n" + str(wall_placement))
    #     #polyline = create_ifcpolyline(self.model, [(0.0, 0.0, 0.0), (5.0, 0.0, 0.0)])
    #     #axis_representation = self.model.createIfcShapeRepresentation(self.context, "Axis", "Curve2D", [polyline])

    #     # Add a new wall-like body geometry, 5 meters long, 3 meters high, and 200mm thick
    #     representation = run("geometry.add_wall_representation", self.model, context=self.body, length=wall_length, height=wall_height, thickness=wall_thickness)
    #     # Assign our new body geometry back to our wall
    #     run("geometry.assign_representation", self.model, product=wall, representation=representation)
    #     # Place our wall in the ground floor
    #     run("spatial.assign_container", self.model, relating_structure=self.storey, product=wall)

    #     print(self.model.to_string())

    def create_2pt_wall(self, p1, p2, elevation, height, thickness, container, wall_type=None):
        p1 = np.array([p1[0],p1[1]])
        p2 = np.array([p2[0],p2[1]])
        def get_angle(p1, p2):
            a = p2 - p1
            x = np.array([1, 0])
            inner = np.inner(a, x)
            norms = np.linalg.norm(a) * np.linalg.norm(x)
            cos = inner / norms
            return np.arccos(np.clip(cos, -1.0, 1.0))

        wall = run("root.create_entity", self.model, ifc_class="IfcWall")
        length = float(np.linalg.norm(p2 - p1))
        representation = run("geometry.add_wall_representation", self.model, context=self.body, length=length, height=height, thickness=thickness)
        a = get_angle(p1, p2)
        sa = np.sin(a)
        ca = np.cos(a)
        matrix = np.array([
            [ca, -sa, 0, p1[0]],
            [sa, ca, 0, p1[1]],
            [0, 0, 1, elevation],
            [0, 0, 0, 1],
        ])
        run("geometry.edit_object_placement", self.model, product=wall, matrix=matrix)
        run("geometry.assign_representation", self.model, product=wall, representation=representation)

        run("spatial.assign_container", self.model, relating_structure=container, product=wall)
        if wall_type:
            run("type.assign_type", self.model, related_object=wall, relating_type=wall_type)

    def get_model(self):
        return self.model
