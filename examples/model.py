import ifcopenshell
from ifcopenshell.api import run
import random

class Model:
    model = None
    body = None
    storey = None

    def create_empty_model(self):
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

    def create_wall(self):
        wall_length = random.randrange(50)
        wall_height = random.randrange(20)
        wall_thickness = 0.2

        # Let's create a new wall
        wall = run("root.create_entity", self.model, ifc_class="IfcWall")
        # Add a new wall-like body geometry, 5 meters long, 3 meters high, and 200mm thick
        representation = run("geometry.add_wall_representation", self.model, context=self.body, length=wall_length, height=wall_height, thickness=wall_thickness)
        # Assign our new body geometry back to our wall
        run("geometry.assign_representation", self.model, product=wall, representation=representation)
        # Place our wall in the ground floor
        run("spatial.assign_container", self.model, relating_structure=self.storey, product=wall)

    def get_model(self):
        return self.model
