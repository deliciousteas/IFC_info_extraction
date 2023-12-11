import ifcopenshell
from OCC.Display.SimpleGui import init_display
from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Display.OCCViewer import rgb_color
from OCC.Extend.ShapeFactory import make_wire
if __name__ == '__main__':
    display, start_display, add_menu, add_function_to_menu = init_display()
    P0=gp_Pnt(0,0,1)
    P1 =gp_Pnt(0, 30, 20)
    display.DisplayShape(P0)
    display.DisplayShape(P1)
    my_box = BRepPrimAPI_MakeBox (P1,10,10,10).Shape()
    display.DisplayShape(my_box,update=True,color=rgb_color(0,1,0))
    start_display()


