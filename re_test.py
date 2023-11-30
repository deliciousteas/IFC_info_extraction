import ifcopenshell
import re
if __name__ =='__main__':
 model=ifcopenshell.open("D:\CimTestFile\SZW_HRZB_MEP_2F.ifc")
 print(model.by_type('IfcProject'))
 #列表list 以逗号分割
 # tmp=model.by_type('IfcProject').split(",")
 print(type(model.by_type('IfcProject')))
 print(model.by_type('IfcProject')[0])
 print(type(model.by_type('IfcProject')[0]))
 tmp=model.by_type('IfcProject')[0]
 print(tmp.Name)