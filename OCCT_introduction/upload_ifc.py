import os
import sys
from OCC.Core.gp import gp_Vec
from OCC.Core.Quantity import  Quantity_Color,Quantity_TOC_RGB
from OCC.Core.Graphic3d import Graphic3d_ClipPlane

from OCC.Display.SimpleGui import init_display

import ifcopenshell
import ifcopenshell.geom


#init_display的四个返回值
display, start_display, add_menu, add_function_to_menu = init_display()
#ifcopenshell gem model
settings=ifcopenshell.geom.settings()
settings.set(settings.USE_PYTHON_OPENCASCADE,True)
print("Loading IFC file",end=" ")
ifc_path=("D:\IFCOpenshell_python_version\Anaconda_ifc\IFC-source\walltest2.ifc")
model=ifcopenshell.open(ifc_path)
print("Loading Done!")


clip_plane_1=Graphic3d_ClipPlane()
clip_plane_1.SetCapping(True)
clip_plane_1.SetCappingHatch(True)
clip_plane_1.SetOn(False)
aMat = clip_plane_1.CappingMaterial()
aColor = Quantity_Color(0.5, 0.6, 0.7, Quantity_TOC_RGB)
aMat.SetAmbientColor(aColor)
aMat.SetDiffuseColor(aColor)
clip_plane_1.SetCappingMaterial(aMat)

wall=model.by_type("IfcWall")[0]
print(wall)
pdct_shape=ifcopenshell.geom.create_shape(settings,inst=wall)
r, g, b, a = pdct_shape.styles[0]  # the shape color
color = Quantity_Color(abs(r), abs(g), abs(b), Quantity_TOC_RGB)
new_ais_shp = display.DisplayShape(
                pdct_shape.geometry,
                color=color,
                transparency=abs(1 - a),
                update=False,
            )[0]
new_ais_shp.AddClipPlane(clip_plane_1)
def animate_translate_clip_plane(event=None):
    clip_plane_1.SetOn(True)
    plane_definition = clip_plane_1.ToPlane()  # it's a gp_Pln
    h = 0.01
    for _ in range(1000):
        plane_definition.Translate(gp_Vec(0.0, 0.0, h))
        clip_plane_1.SetEquation(plane_definition)
        display.Context.UpdateCurrentViewer()
if __name__ == "__main__":
    add_menu("IFC clip plane")
    add_function_to_menu("IFC clip plane", animate_translate_clip_plane)
    display.FitAll()
    start_display()



