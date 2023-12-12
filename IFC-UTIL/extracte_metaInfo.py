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
    space=model.by_type("IfcSpace")
    #第一次ids是ids，
    str_list=[]
    str_list.append(project[0])
    str_list.append(site[0])
    if len(space)!=0:
        str_list.append(space[0])
    for i in range(len(building)):
        str_list.append(building[i])
    for i in range(len(sotrey)):
        str_list.append(sotrey[i])
    #提取spatcial_structure 的reference id,第二次输出的是ids的引用id
    print(str_list)
    tmp_list = []
    # 添加IfcSite、building、storey和project之间的空间结构
    # end:product 和building之间的关系从product的ContainedInstructure、ReferencedInstructures拿
    for i in range(len(str_list)):
        print(str_list[i].is_a())
        if len(str_list[i].IsDecomposedBy) != 0:
            tmp_list.append(str_list[i].IsDecomposedBy[0])
        if len(str_list[i].Decomposes) != 0:
            tmp_list.append(str_list[i].Decomposes[0])
        # if str_list[i].is_a() != "IfcProject":
        #     if len(str_list[i].ContainsElements) != 0:
        #         print(str_list[i].ContainsElements)
        #         tmp_list.append(str_list[i].ContainsElements[0])
        # if len(str_list[i].ServicedBySystems) != 0:
        #     str_list.append(str_list[i].ServicedBySystems[0])
        # if len(str_list[i].ReferencesElements) != 0:
        #     str_list.append(str_list[i].ReferencesElements[0])
    print(tmp_list)
    for x in range(len(tmp_list)):
        str_list.append(tmp_list[x])
    # print(str_list)
    str_list = list(set(str_list))
    # print(str_list)
    # 提取spaticial stucture上的反属性关系，IFcRelaggregates

    ids = []
    for j in range(len(str_list)):
        # print(extracte_ids(str(str_list[j])))
        tmp_ids = extracte_ids(str(str_list[j]))
        for i in range(1, len(tmp_ids)):
            ids.append(tmp_ids[i])
        ids = list(set(ids))
    print(ids)
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
    #todo 太慢了，提取内容，都是大O(n平方)的过程，可以考虑先set后再考虑id号查询
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
fucntion:提取entity中一个instance的位置和构形以及历史版本信息
para：绝对路径，ifc ，entity-type

可以接受改成提取多个instance的位置和构形
"""
def extracte_entity_structure(path_file,type):

    model = ifcopenshell.open(path_file)
    instances = model.by_type(type)
    #test just one
    instance = instances[0]
    instance_id = instance.id()
    instance_text = str(instance)
    ids = extracte_ids(instance_text)[1:]
    #print(ids)
    #ids是它的引用，instance_id是它的id
    ids.insert(0,instance_id)
    #这里的id是他自身和它的直接引用
    print(ids)
    graph=model_graph(path_file,ids,None)
    all_key = list(graph.keys())
    all_value = [val for sublist in graph.values() for val in sublist]
    entity_infoList = list(set(all_key + all_value))
    #添加第i个instance的RelatedElements,!!!只需要添加一次就好。
    entity_infoList.append(instance.ContainedInStructure[0].id())
    return entity_infoList

"""
测试多个instances啊！！！！！！！！
fucntion:提取entity中所有instance的位置和构形以及历史版本信息
para：绝对路径，ifc ，entity-type，all_instance，如果为true就提取所有的，如果为false，就只提取一个

可以接受改成提取多个instance的位置和构形
"""


def extracte_entity_structure(path_file,type,all_instance):
     model = ifcopenshell.open(path_file)
     instances = model.by_type(type)
     if all_instance==True:
         all_instance_list=[]
         for i in range(len(instances)):
             instance=instances[i]
             instance_id = instance.id()
             instance_text = str(instance)
             ids = extracte_ids(instance_text)[1:]
             ids.insert(0, instance_id)
             for j in range(len(ids)):
                all_instance_list.append(ids[j])
         all_instance_list=list(set(all_instance_list))
         graph = model_graph(path_file, all_instance_list, None)
         all_key = list(graph.keys())
         all_value = [val for sublist in graph.values() for val in sublist]
         all_List = list(set(all_key + all_value))
         all_List.append(instances[0].ContainedInStructure[0].id())
         return all_List
     else:
         instance = instances[0]
         instance_id = instance.id()
         instance_text = str(instance)
         ids = extracte_ids(instance_text)[1:]
         # print(ids)
         # ids是它的引用，instance_id是它的id
         ids.insert(0, instance_id)
         # 这里的id是他自身和它的直接引用
         print(ids)
         graph = model_graph(path_file, ids, None)
         all_key = list(graph.keys())
         all_value = [val for sublist in graph.values() for val in sublist]
         entity_infoList = list(set(all_key + all_value))
         # 添加第i个instance的RelatedElements,!!!只需要添加一次就好。
         entity_infoList.append(instance.ContainedInStructure[0].id())
         return entity_infoList






if __name__ == '__main__':

    #extract spatcial info

    print(extracte_project_structure("..\data\SZW_RFJD_ARC_1F.ifc"))
    #extracte prodcut-levl info

    print(extracte_entity_structure("..\data\SZW_RFJD_ARC_1F.ifc", "IfcDoor"))
