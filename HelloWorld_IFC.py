import ifcopenshell
import ifcopenshell.util
import ifcopenshell.util.element
import multiprocessing

import ifcopenshell.geom
import ifcopenshell.util.pset
from ifcopenshell import util


"""
std cout：
   schema:IFC版本号
   ifcproject：项目名称、几何表示精度、维度、坐标原点（估计WGS84、正北方向
   ifcsite:经纬度、海拔基准
   ifcspace:描述footprint的没有，只能自己找
   

"""
def Get_ProjectInfo(model_path):

   instance=ifcopenshell.open(model_path)
   schema=instance.schema
   print('schema : %s'%schema)
   project_info=instance.by_type('IfcProject')[0]
   Name=project_info.Name
   LongName=project_info.LongName
   #product‘s whole environment belows.
   ReresentationContexts=project_info.RepresentationContexts
   Units=project_info.UnitsInContext
   print('Name: %s ,LongName: %s ,'%(Name,LongName))
   #todo，如果ReresentationContexts》1需要重新写
   #输出维度、精度、正北方向、世界坐标系原点
   if(len(ReresentationContexts)>1):
      print(ReresentationContexts[0].CoordinateSpaceDimension)
      print(ReresentationContexts[0].Precision)
      print(ReresentationContexts[0].WorldCoordinateSystem)
      print(ReresentationContexts[0].TrueNorth)

      print(ReresentationContexts[1].CoordinateSpaceDimension)
      print(ReresentationContexts[1].Precision)
      print(ReresentationContexts[1].WorldCoordinateSystem)
      print(ReresentationContexts[1].TrueNorth)
   else:
      WorldCoordinateSystem=ReresentationContexts[0].WorldCoordinateSystem.Location.Coordinates
      TrueNorth=ReresentationContexts[0].TrueNorth.DirectionRatios
      print('CoordinateSpaceDimension: %d,Precision: %d,WorldCoordinateSystem: %s,TrueNorth:%s'%(ReresentationContexts[0].CoordinateSpaceDimension,ReresentationContexts[0].Precision,WorldCoordinateSystem,TrueNorth))

   Site=instance.by_type('IfcSite')
   Space=instance.by_type('IfcSpace')
   print('RefLatitude:%s ,RefLongitude:%s ,RefElevation: %d'%(Site[0].RefLatitude,Site[0].RefLongitude,Site[0].RefElevation))
   print("objectPlacement:%s ,Representation:%s"%(Site[0].ObjectPlacement,Site[0].Representation))
   print('Space：%s'%Space)
   print("----------------------------")

"""
IfcBuilding：高度、海拔
todo：查看地址、位置。
反属性都是无关没有填写的信息。

"""
def Get_BuildingInfo(Model_path):
   model = ifcopenshell.open(Model_path)
   instance=model.by_type("IfcBuilding")
   for i in range(0,len(instance)):
      Height=instance[i].ElevationOfRefHeight
      Terrain=instance[i].ElevationOfTerrain
      Address=instance[i].BuildingAddress
      Placement=instance[i].ObjectPlacement
      print('Height: %s,Terrain: %s ,Address: %s,Placement: %s'%(Height,Terrain,Address,Placement))
   print("----------------------------")
   #反属性存储链接关系,IsDefinedBy、IsTypedBy

   # if(instance[0].IsDefinedBy!=0):
   #    Definedprperty_set = []
   #    for i in range(0, len(instance[0].IsDefinedBy)):
   #       Definedprperty_set.append(instance[0].IsDefinedBy[i].RelatingPropertyDefinition)
   #    print(Definedprperty_set)
   #    for i in range(0,len(Definedprperty_set)):
   #       propertyset_number=Definedprperty_set[i].HasProperties
   #       print(propertyset_number)
   #
   #    for j in range(0, len(Definedprperty_set)):
   #       test = Definedprperty_set[j]
   #    for x in range(0, len(test.HasProperties)):
   #       print(test.HasProperties[x])
   #       print(test.HasProperties[x].Name)
   #       print(test.HasProperties[x].NominalValue)
   #    print("-------------------------------")
   # if(instance[0].IsTypedBy!=0):
   #    Typedproerty_set = []
   #    for i in range(0, len(instance[0].IsTypedBy)):
   #       Typedproerty_set.append(instance[0].IsTypedBy[i].RelatingPropertyDefinition)
   #    print(Typedproerty_set)


"""
Ifcbuildingstrey：楼层名字、海拔高度、局部坐标、IfcDefinedInfo（没用就不输出）
需要返回N N+1的楼层localplacement值，计算完换算单位。
完成site-building-buildingstorey之间的坐标转换。
"""
def Get_storey(model_path):
   model=ifcopenshell.open(model_path)
   instance=model.by_type("IfcBuildingStorey")
   # 一般是跨层的。
   for i in range (0,len(instance)):

      print(instance[i])
      name=instance[i].Name
      elevation=instance[i].Elevation
      print('Name:%s,Elevation: %s' % (name, elevation))
      ObjectPlacement=(instance[i].ObjectPlacement)

      #IfcLocalPlacement，定义参考坐标系，使用的局部坐标系?,par1：参考坐标系，par2 相对于par1的坐标转换
      print(ObjectPlacement)
      Storey_cited_coor=ObjectPlacement.PlacementRelTo
      Storey_cited_trans=ObjectPlacement.RelativePlacement.Location
      print('buildingStorey参考: %s ,transofrmation:%s'%(Storey_cited_coor,Storey_cited_trans))

      building_cited_coor=Storey_cited_coor.PlacementRelTo
      building_cited_trans=Storey_cited_coor.RelativePlacement.Location
      print('building参考: %s ,transofrmation:%s' % (building_cited_coor, building_cited_trans))

      site_cited_coor=building_cited_coor.PlacementRelTo
      site_cited_trans=building_cited_coor.RelativePlacement.Location
      print('site参考: %s ,transofrmation:%s' % (site_cited_coor, site_cited_trans))

      print("----------------------------")
      #IsDefinedby INVERSE ATTRIBUTE,可能反属性中没有quantity 属性
      # property sets can by assigned to occurrence objects or an object type
      #IsTypedby,inverse attribute type和type_occurence，共享type的proerty sets
      #object occurrence has a proerty set assigned ,it has priority than shared type property sets
      # area are quantity set attribute

def Get_Slabs(model_path):
   model=ifcopenshell.open(model_path)
   instance=model.by_type("IfcSlab")
   #name | objectType choose one
   for i in range(0,len(instance)):
      print(instance[i])
      Name = instance[i].Name
      ObjectType = instance[i].ObjectType
      # Floor: a floor slab ;Roof: roof slab;Landing: a landing iwthin a stair or ramp;Baseslab:mat foundation
      Type = instance[i].PredefinedType

      # PlaceMENTrETO可以判断是第一层还是第二层的内容
      ObjectPlacement = instance[i].ObjectPlacement

      Representation = instance[i].Representation


      print('IfcSlab的Name：%s, Type: %s ,Specified Type: %s, Location: %s,Representation:%s'%(Name,ObjectType,Type))
      #关于objection
      #todo：需要考虑反属性
      print('IFcSlab的参考坐标系：%s ,局部坐标系： %s,坐标位于： %s'%(ObjectPlacement.PlacementRelTo,ObjectPlacement.RelativePlacement,ObjectPlacement.RelativePlacement.Location))
      #关于representation
      #todo:需要考虑反属性
      print('IfcSlab的Representation Name:%s ,Description: %s,Representations:%s'%(Representation.Name,Representation.Description,Representation.Representations))


      print("-----------------------------------------------")



if __name__ =='__main__':



 print('接下来输出该IFC项目的项目基本信息：')

 #todo 格式化存储在在txt文件中中。ifcplacement记录了非常多的1W多条
 #todo 将坐标信息存储在楼层这个层次？
 #todo 提取ifcductsegment所有instance
Get_ProjectInfo("D:\CimTestFile\SZW_RFJD_ARC_1F.ifc")
Get_BuildingInfo("D:\CimTestFile\SZW_RFJD_ARC_1F.ifc")
Get_storey("D:\CimTestFile\SZW_RFJD_ARC_1F.ifc")
Get_Slabs("D:\CimTestFile\SZW_RFJD_ARC_1F.ifc")