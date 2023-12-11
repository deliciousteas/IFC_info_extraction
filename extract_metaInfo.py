import ifcopenshell

if __name__ =='__main__':
    model=ifcopenshell.open("D:\CimTestFile\SZW_RFJD_ARC_1F.ifc")
    print(model.by_type("IfcProject")[0])
    print(model.by_type("Ifcsite")[0])
    print(model.by_type("IfcBuilding")[0])
    print(model.by_type("IfcBuildingStorey"))
    wall=model.by_type("IfcWall")[0]
    print(wall.ReferencedInStructures)
    #这个信息是需要的,len（）长度里面有不是ifcwall的，它是把这一层包含的建筑信息全部记录在里面。
    print(wall.ContainedInStructure[0].id())
    print(len(wall.ContainedInStructure[0].RelatedElements))
    site=model.by_type("Ifcsite")[0]
    print(site.IsDecomposedBy)
    print(site.Decomposes)