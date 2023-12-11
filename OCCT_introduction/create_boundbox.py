from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import  brepbndlib_Add
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.gp import gp_Pnt
from OCC.Display.SimpleGui import init_display
import ifcopenshell.geom
import ifcopenshell

from OCC.Core.TopoDS import TopoDS_Compound, TopoDS_Shape

"""
BRepPrimAPI_MakeBox:CONSTRUCTOR
继承关系：class BRepPrimAPI_MakeBox(OCC.Core.BRepBuilderAPI.BRepBuilderAPI_MakeShape):
para：
    dx dy dz 参数表示在x yz轴上的位移；
    optional:P: gp_Pnt类型，点位
    optional:p1,p2：多个gp_pnt类型
    optional:Axes: gp_Ax2(gp_AX2表示坐标轴，由（原点gp_Pnt，和三个轴的方向gp_dir）组成。)

BRepPrimAPI_MakeCylinder
Cylinder 圆柱圆筒
para:
r:radius
h:height
angles是角度
Axes：描述的是坐标轴

BRepMesh_IncrementalMesh
用于Mesh网格化的嘞，由一些点线面组成的离散数据结构，表示几何体的表面。mesh可以将几何体转为网格。
"""
"""
得到的ifc控件是TopoDS_Compound类型
"""

if __name__ == '__main__':

    ifc_path = ("D:\IFCOpenshell_python_version\Anaconda_ifc\IFC-source\walltest2.ifc")
    model = ifcopenshell.open(ifc_path)

    # return an Brep model from ifc file
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True)
    wall = model.by_type("IfcWall")[0]
    # create a rough shape,*.geometry method will make this shape to TopoDS_Compound
    # thus return TopoDS_Compound INSTANCE
    wall_create_shape = ifcopenshell.geom.create_shape(settings, inst=wall)
    wall_shape=wall_create_shape.geometry

    # CONNECT wall_shape with bound_box
    compound_box=Bnd_Box()
    brepbndlib_Add(wall_shape,compound_box)

    corner_min=compound_box.CornerMin()
    corner_max=compound_box.CornerMax()
    # 在显示窗口中显示立方体
    display, start_display, add_menu, add_function_to_menu = init_display()
    display.DisplayShape(wall_shape,color="WHITE")
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
    # 适应内容并启动显示窗口
    display.FitAll()
    start_display()