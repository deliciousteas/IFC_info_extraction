import ifcopenshell

if __name__ =='__main__':
    model=ifcopenshell.open("D:\CimTestFile\SZW_RFJD_ARC_1F.ifc")
    print(model.by_type("IfcProject")[0])
    print(model.by_type("Ifcsite")[0])
    print(model.by_type("IfcBuilding")[0])
    print(model.by_type("IfcBuildingStorey"))