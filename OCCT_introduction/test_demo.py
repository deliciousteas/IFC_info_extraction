from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.gp import gp_Pnt
from OCC.Display.OCCViewer import rgb_color

TOL = 1e-4

shape = BRepPrimAPI_MakeCylinder(60, 60, 50).Shape()
# shape = read_iges_file("robot_arm.igs")
tol = TOL   # tol = TOL (by default)
bbox = Bnd_Box()
bbox.SetGap(tol)

mesh = BRepMesh_IncrementalMesh(shape, tol, True)
mesh.Perform()
# this is adds +margin but is faster
brepbndlib_Add(shape, bbox, True)

XMin, YMin, ZMin, XMax, YMax, ZMax = bbox.Get()

xmin = XMin
xmax = XMax
xlen = XMax - XMin
ymin = YMin
ymax = YMax
ylen = YMax - YMin
zmin = ZMin
zmax = ZMax
zlen = ZMax - ZMin

center = gp_Pnt((XMax + XMin) / 2,
                     (YMax + YMin) / 2,
                     (ZMax + ZMin) / 2)

box = BRepPrimAPI_MakeBox(gp_Pnt(xmin,ymin,zmin),gp_Pnt(xmax,ymax,zmax)).Shape()


if __name__ == "__main__":
    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()
    print(xmin)
    print(xmax)
    display.DisplayShape(shape)
    display.DisplayShape(box,update=True,color=rgb_color(0,0,0.1),transparency=1)
    start_display()
