import os.path
import extracte_metaInfo
import ifcopenshell

"""
extracete HEADER info from an *.ifc until it read DATA;
para:*.ifc file absolute path
"""
def extracte_Header_info(path_file):
    with open(path_file,'r')as ifcFile:
        for line in ifcFile:
            print(line)
            if line.strip()=="DATA;":
                break
                ifcFile.close()
def WriteNewFIle(path_file,save_path,filename):
    file_path=os.path.join(save_path,filename)
    model=ifcopenshell.open(path_file)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"DELETED EXISTING FILE:{filename}")
    with open(file_path,'w')as new_file:
        with open(path_file,'r')as source_file:
            for line in source_file:
                new_file.write(line)
                if line.strip()=="DATA;":
                    break
            source_file.close()
            new_file.write("\n")
            # add product and project info
            project_ids=extracte_metaInfo.extracte_project_structure(path_file)
            print(project_ids)

            #可更改测试所有entity还是单个entity
            prudtct_ids=extracte_metaInfo.extracte_entity_structure(path_file,"IfcWall",True)
            print(prudtct_ids)
            list_all=[]
            for i in range(len(project_ids)):
                list_all.append(project_ids[i])
            for i in range(len(prudtct_ids)):
                list_all.append(prudtct_ids[i])
            list_all=list(set(list_all))
            print(list_all)
            for j in range(len(list_all)):
                instance = str(model.by_id(list_all[j]))
                new_file.write(instance + ';' + '\n')
            # for i in  range(len(project_ids)):
            #     instance = str(model.by_id(project_ids[i]))
            #     new_file.write(instance+';'+'\n')
            # for j in range(len(prudtct_ids)):
            #     instance = str(model.by_id(prudtct_ids[j]))
            #     new_file.write(instance + ';'+'\n')
            new_file.write("\n")
            new_file.write("ENDSEC;\n")
            new_file.write("END-ISO-10303-21;")
        new_file.close()
    print(f"New IFC file created here: {file_path}")


if __name__ == '__main__':
    WriteNewFIle("..\data\SZW_RFJD_ARC_1F.ifc","..\output","Wall.ifc")