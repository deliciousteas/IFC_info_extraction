import ifcopenshell
import ifcopenshell.util
import re
""""
store produt-level info by directed graph...

"""


pattern='''^#\d+'''
def Extrate_productINFO(path,entity):
    model=ifcopenshell.open(path)
    instance_list=model.by_type(entity)
    for i in range(0,len(instance_list)):
        if instance_list[i].ObjectPlacement is not None and instance_list[i].Representation is not None:
            if i<=1:
                #placement
                #print(instance_list[i].ObjectPlacement)
                #Reprensentation
                Representation_1=instance_list[i].Representation
                #print(Representation_1)
                if(len(Representation_1.Representations)==0):
                    print("without Presentation")
                else:
                    Representation_2 = Representation_1.Representations
                    #depth 可能有1也可能大于2
                    for i in range(0,len(Representation_2)):

                        print(Representation_2[i])
                        #存储属性的文本描述,type is class
                        print(Representation_2[i].RepresentationIdentifier)
                        print(Representation_2[i].RepresentationType)
                        # item有差别。
                        if(Representation_2[i].RepresentationIdentifier=='Axis'):
                            print(Representation_2[i].Items)










if __name__ =='__main__':
    Extrate_productINFO("D:\CimTestFile\SZW_RFJD_ARC_1F.ifc","IfcWall")