
from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
import ifcopenshell.geom
import time
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.Bnd import Bnd_OBB
from OCC.Core.TopoDS import topods
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.gp import gp_Pnt
display, start_display,add_menu, add_function_to_menu = init_display()
if __name__ == '__main__':

    ifc_path = ("D:\IFCOpenshell_python_version\Anaconda_ifc\IFC-source\walltest2.ifc")
    model = ifcopenshell.open(ifc_path)

     #return an Brep model from ifc file
    settings=ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE,True)
    wall=model.by_type("IfcWall")[0]
    wall_shape=ifcopenshell.geom.create_shape(settings,inst=wall)

    #upload ifcwall
    view_wall=display.DisplayShape(wall_shape.geometry)[0]


    #display
    add_menu("目录")
    #add_function_to_menu需要提供function内容，function需要是可调用的方法或者是嘞
    #add_function_to_menu("nihao",Geek)
    display.FitAll()

    time.sleep(10)
    start_display()
    input("presee enter to exis.")


