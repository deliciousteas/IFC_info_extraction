import  ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.placement
import math
from OCC.Core.BRepGProp import brepgprop_VolumeProperties, brepgprop_SurfaceProperties
from OCC.Core.GProp import GProp_GProps
import ifcopenshell.util.shape

import tripy
import pythreejs as p3js
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

"""
this module is  trying to compute geometry property of an product-level-ifc file.(gain a product-level ifc file after write_newfile.py)
here are its methods:
1. description:
amount of product-level,location and height
2. property
volume,2-d area,
todo:
boundbox ,adn calculate city-level's 指标
"""
def get_description(path_file:str,entity_type:str):
    model=ifcopenshell.open(path_file)
    instances=model.by_type(entity_type)
    if len(instances)!=0:
        Amount=len(instances)
    description_list={}
    for i in range(len(instances)):
        matrix = ifcopenshell.util.placement.get_local_placement(instances[i].ObjectPlacement)
        #print(matrix)
        id=instances[i].id()
        Globalid=instances[i].GlobalId
        description_list[i] = []
        description_list[i].append({"id":id,"GlobalId":Globalid,"coordination":matrix[:,3][:3]})

    return Amount,description_list

def output_descprition(path_file:str,entity_type:str):
    Amount,description_list=get_description(path_file,entity_type)
    print(path_file+" has "+str(Amount)+" "+entity_type)
    print("their id,globalid,location belows:")
    print(description_list)
    # coordination_value = description_list[0][0]['coordination']
    #
    # print(coordination_value)



def Distance_2D(path_file:str,entity_type:str,entity1:int,entity2:int):
    Amount,dic=get_description(path_file,entity_type)
    print(dic[1])
    print(dic[10])
    coor1=dic[entity1][0]['coordination']
    coor2=dic[entity2][0]['coordination']
    print(f"{entity1}的坐标是{coor1},{entity2}的坐标是{coor2}")
    distance=math.sqrt((coor1[0]-coor2[0])**2+(coor1[1]-coor2[1])**2)
    print(f"{entity1}和{entity2}之间的2维距离是：{distance}")


"""对字典中中的第i个计算体积"""
def get_Volume_and_Area(path_file:str,entity_type:str,dic_int:int):
    amount,dic=get_description(path_file,entity_type)
    model=ifcopenshell.open(path_file)
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True)
    #print(dic[dic_int][0]['id'])
    instance=model.by_id(dic[dic_int][0]['id'])
    #print(instance)

    # column volume and area
    instance_create_shape = ifcopenshell.geom.create_shape(settings, inst=instance)
    instance_shape = instance_create_shape.geometry
    gprops1 = GProp_GProps()
    grops2= GProp_GProps()
    volume_props=brepgprop_VolumeProperties(instance_shape,gprops1)
    volume=gprops1.Mass()
    surface_props = brepgprop_SurfaceProperties(instance_shape,grops2)
    surface_area = grops2.Mass()
    print("体积:", volume)
    print("表面积:", surface_area)

"""
obtain one instance's vertex、edges、faces and its location
"""
def get_Shape_component(path_file,entity_type):
    model=ifcopenshell.open(path_file)
    instances=model.by_type(entity_type)

    #test just one
    instance=instances[0]
    settings = ifcopenshell.geom.settings()
    shape = ifcopenshell.geom.create_shape(settings, instance)

    # vertex(x,y,z),edge(v1,v2),face(v1,v2,v3)
    #difference between verts and get_vertices is the precision
    # vertexs=shape.geometry.verts
    # edges=shape.geometry.edges
    # faces=shape.geometry.faces
    matrix=ifcopenshell.util.shape.get_shape_matrix(shape)
    location=matrix[:,3][0:3]
    grouped_verts = ifcopenshell.util.shape.get_vertices(shape.geometry)
    grouped_edges = ifcopenshell.util.shape.get_edges(shape.geometry)
    grouped_faces = ifcopenshell.util.shape.get_faces(shape.geometry)
    print(grouped_edges)
    print(grouped_faces)
    print(grouped_verts)
    return grouped_verts,grouped_edges,grouped_faces

"""
todo:需不需要将ifc转为mesh结构，然后再计算指标。
"""
def create_mesh(path_file,entity_type):
    print("你好")



if __name__ == '__main__':

   # output_descprition("../output/Wall.ifc","IfcWall")
   # Distance_2D("../output/Wall.ifc","IfcWall",2,206)
   # get_Volume_and_Area("../output/Wall.ifc","IfcWall",10)
   #get_Shape_component("../output/Wall.ifc","IfcWall")
   create_mesh("../output/DOOR1.ifc","IfcDoor")
   print("你好")