from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import  brepbndlib_Add
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.gp import gp_Pnt
from OCC.Display.SimpleGui import init_display
import ifcopenshell.geom
import ifcopenshell
from OCC.Core.TopoDS import TopoDS_Compound, TopoDS_Shape
from OCC.Core.BRepGProp import brepgprop_VolumeProperties, brepgprop_SurfaceProperties
from OCC.Core.GProp import GProp_GProps


"""
test uploade ifcwall and its boundbox
"""
if __name__ == '__main__':
    model=ifcopenshell.open("../output/Wall.ifc")
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True)
    Wals=model.by_type("IfcWall")
    nb_of_Walls=len(Wals)
    compound_box=Bnd_Box()
    for i ,wall in enumerate(Wals):
        #print(i)
        wall_create_shape = ifcopenshell.geom.create_shape(settings, inst=wall)
        r, g, b, a = wall_create_shape.styles[0]  # the shape color
        wall_shape=wall_create_shape.geometry
        brepbndlib_Add(wall_shape, compound_box)

    # 获取整体包围盒的角点坐标
    corner_min = compound_box.CornerMin()
    corner_max = compound_box.CornerMax()

    display, start_display, _, _ = init_display()
    # 在显示窗口中显示整体包围盒
    display.DisplayShape(corner_min, color="WHITE")
    display.DisplayShape(corner_max, color="WHITE")
    display.FitAll()

    for wall in model.by_type("IfcWall"):
        wall_create_shape = ifcopenshell.geom.create_shape(settings, inst=wall)
        wall_shape = wall_create_shape.geometry
        display.DisplayShape(wall_shape, color="BLUE")

    # 可视化整体包围盒的立方体边框
    vertices = [gp_Pnt(corner_min.X(), corner_min.Y(), corner_min.Z()),
                gp_Pnt(corner_max.X(), corner_min.Y(), corner_min.Z()),
                gp_Pnt(corner_max.X(), corner_max.Y(), corner_min.Z()),
                gp_Pnt(corner_min.X(), corner_max.Y(), corner_min.Z()),
                gp_Pnt(corner_min.X(), corner_min.Y(), corner_max.Z()),
                gp_Pnt(corner_max.X(), corner_min.Y(), corner_max.Z()),
                gp_Pnt(corner_max.X(), corner_max.Y(), corner_max.Z()),
                gp_Pnt(corner_min.X(), corner_max.Y(), corner_max.Z())]

    for vertex in vertices:
        display.DisplayShape(vertex, color="GREEN")

    for i in range(4):
        edge = BRepBuilderAPI_MakeEdge(vertices[i], vertices[(i + 1) % 4]).Edge()
        display.DisplayShape(edge, color="RED")

        edge = BRepBuilderAPI_MakeEdge(vertices[i + 4], vertices[((i + 1) % 4) + 4]).Edge()
        display.DisplayShape(edge, color="RED")

        edge = BRepBuilderAPI_MakeEdge(vertices[i], vertices[i + 4]).Edge()
        display.DisplayShape(edge, color="RED")

    # 展示整体包围盒
    display.FitAll()
    start_display()

