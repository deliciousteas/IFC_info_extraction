import ifcopenshell

if __name__ =='__main__':
    model=ifcopenshell.open("D:\CimTestFile\SZW_RFJD_ARC_1F.ifc")
    print(model.by_type("IfcProject")[0])
    print(model.by_type("Ifcsite")[0])
    print(model.by_type("IfcBuilding")[0])
    print(model.by_type("IfcBuildingStorey"))
    print(model.by_type("IfcProject")[0].IsDecomposedBy[0])
    print(model.by_type("IfcProject")[0].Decomposes)
    print(len(model.by_type("IfcProject")[0].Decomposes))
    if model.by_type("IfcProject")[0].Decomposes !="()":
        print("hhhhh")

    instace=model.by_type("IfcWall")[0]
    print(instace)
    print(instace.IsDecomposedBy)
    print(instace.Decomposes)
    print(model.by_type("IfcBuildingStorey")[0])
    ins=model.by_type("IfcBuildingStorey")[0]
    print(ins.ContainsElements)
    print(ins.ServicedBySystems)
    print(ins.ReferencesElements)
    test=model.by_type("IfcWall")[0]
    #todo：这里可以获取它的所有同类
    #print(test.ContainedInStructure)