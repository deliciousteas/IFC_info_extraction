import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.placement
import ifcopenshell.util.shape
import ifcopenshell.util.element

ifc_instance=ifcopenshell.open("D:\CimTestFile\SZW_RFJD_ARC_1F.ifc")

"""
function:
    create a shape by opencascade,if entity's instance has any Representation
para:
    setting: default is OPENCASCADE 
    inst:entity's instance
"""
settings = ifcopenshell.geom.settings()
walls=ifc_instance.by_type("IfcWall")
for i ,wall in enumerate(walls):
    if wall.Representation is not None:
        shape=ifcopenshell.geom.create_shape(settings,wall)
        if 0<i<=5:
            # Representation's location and rotation of this element
            matrix=ifcopenshell.util.shape.get_shape_matrix(shape)
            #print(matrix)

            #XYZ LOCATION
            location=matrix[:,3][0:3]
            print(location)

            #verts、edges、faces
            grouped_verts=ifcopenshell.util.shape.get_vertices(shape.geometry)
            grouped_edges = ifcopenshell.util.shape.get_edges(shape.geometry)
            grouped_faces=ifcopenshell.util.shape.get_faces(shape.geometry)
            print(f"element的vertex各为{grouped_verts}")
            print(f"element的edge各为{grouped_edges}")
            print(f"element的face各为{grouped_faces}")











# matrix=shape.transformation.matrix.data
# matrix=ifcopenshell.util.shape.get_shape_matrix(shape)






