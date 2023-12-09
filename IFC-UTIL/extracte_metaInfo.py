import ifcopenshell
import re


"""
extracte instance's reference ids and delete '#' 
par:text ，such as #1=IFCORGANIZATION($,'Autodesk Revit 2023 (CHS)',$,$,$);
return:such as,[34，54，75]
"""
def extracte_ids(text):
    pattern=r'#\d+'
    return [int(match[1:])for match in re.findall(pattern,text)]



""""
obtain   *.ifc file's IfcProject IfcSite IfcBuilding  IfcBuildingStorey reference id.
:para:  *.ifc file absolute path such as :"D:\CimTestFile\SZW_RFJD_ARC_1F.ifc"
:return  a list of int element ,this contains project stucture instances'ids and their all referenced ids.
"""
def extracte_project_structure(path_file)-> list:

    model=ifcopenshell.open(path_file)
    project=model.by_type("IfcProject")
    site=model.by_type("IfcSite")
    building=model.by_type("IfcBuilding")
    sotrey=model.by_type("IfcBuildingStorey")
    #第一次ids是ids，
    str_list=[]
    str_list.append(project[0])
    str_list.append(site[0])
    for i in range(len(building)):
        str_list.append(building[i])
    for i in range(len(sotrey)):
        str_list.append(sotrey[i])
    #提取spatcial_structure 的reference id,第二次输出的是ids的引用id
    #print(str_list)
    ids=[]
    for j in range(len(str_list)):
        #print(extracte_ids(str(str_list[j])))
        tmp_ids=extracte_ids(str(str_list[j]))
        for i in range(1,len(tmp_ids)):
            ids.append(tmp_ids[i])
        ids=list(set(ids))

    #print(ids)
    structure=model_graph(path_file,ids,graph=None)
    #print(structure)
    all_key=list(structure.keys())
    all_value=[val for sublist in structure.values() for val in sublist]
    ifclist_tmp=list(set(all_key+all_value))
    #print(ifclist_tmp)
    #将parent_ids和ifclist_tmp合并在一起，reference和本体就都有了
    for h in range(0,len(str_list)):
        ifclist_tmp.append(int(str_list[h].id()))
    return ifclist_tmp

"""
:param
path:*.ifc file absolute path
id_array: instances' reference id list
graph: default is None
:function
extract all reference by recursion.
"""
def model_graph(path_file,id_array,graph=None):

    model=ifcopenshell.open(path_file)
    if graph is None:
        graph = {}
    node_id=int(id_array[0])
    children=id_array[1:]
    graph[node_id] = children
    for i in range(1,len(id_array)):
        instance=str(model.by_id(int(id_array[i])))
        #得到isntance的所有id号
        sub_ids = extracte_ids(instance)
        if len(sub_ids)>=2:
            #print(f"{sub_ids[0]}还有sub节点了")
            #print(graph)
            model_graph(path_file, sub_ids, graph)
        else:
            print(f"{sub_ids[0]}已经是子节点了")

    #print(graph)
    return graph

""""
先测试一个啊！！！！！！！！
fucntion:提取entity中一个instance的位置和构形
para：绝对路径，ifc ，entity-type
"""
def extracte_entity_structure(path_file,type):
    #path=path_file
    model = ifcopenshell.open(path_file)
    instances = model.by_type(type)
    instance = instances[0]
    instance_id = instance.id()
    instance_text = str(instance)
    ids = extracte_ids(instance_text)[1:]
    #print(ids)
    #ids是它的引用，instance_id是它的id
    ids.insert(0,instance_id)
    print(ids)
    #return ids

    graph=model_graph(path_file,ids,None)
    all_key = list(graph.keys())
    all_value = [val for sublist in graph.values() for val in sublist]
    entity_infoList = list(set(all_key + all_value))
    return entity_infoList


if __name__ == '__main__':

    #extract spatcial info

    print(extracte_project_structure("D:\CimTestFile\SZW_RFJD_ARC_1F.ifc"))
    #extracte prodcut-levl info

    print(extracte_entity_structure("D:\CimTestFile\SZW_RFJD_ARC_1F.ifc", "IfcDoor"))
