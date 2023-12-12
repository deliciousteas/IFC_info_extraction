import ifcopenshell
import ifcopenshell.util
import re
import os


def extracte_ids(text):
    pattern=r'#\d+'
    return [int(match[1:])for match in re.findall(pattern,text)]
def build_instance_graph(model,instance_id):
    #todo：serialize info
    instance=model.by_id(instance_id)
    if not instance:
        return None
    instance_text=str(instance)
    ids=extracte_ids(instance_text)
    if ids==1:
        return None
    graph_vertex={}
    for i in range(1,len(ids)):
        sub_instance_ids=int(ids[i])
        graph_vertex[ids[0]]=1
        sub_graph=build_instance_graph(model,sub_instance_ids)
        if sub_graph is not None:
            graph_vertex[sub_instance_ids]=sub_graph

    return graph_vertex if graph_vertex else None
def modl_preprocess(path,type) ->list:
    model=ifcopenshell.open(path)
    instances=model.by_type(type)
    instance=instances[0]
    product_id=instance.id()
    instance_text=str(instance)
    ids=extracte_ids(instance_text)[2:]
    #预处理，去除自己和历史记录，只要两个位置和构形
    vertex_list=[]
    vertex_list.append(product_id)
    for i in range(0,len(ids)):
        vertex_list.append(int(ids[i]))
    return vertex_list
def model_graph(path,id_array,graph=None):

    model=ifcopenshell.open(path)
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
            model_graph(path, sub_ids, graph)
        else:
            print(f"{sub_ids[0]}已经是子节点了")

    #print(graph)
    return graph






def extracte_meta_info(path):
    with open(path,'r')as ifcFile:
        for line in ifcFile:
            print(line)
            if line.strip()=="ENDSEC;":
                break
                ifcFile.close()
    #todo:extract site、project、building info
    #model=ifcopenshell.open(path)
    #site=model.by_type("Ifcsite")
    #project=model.by_type("IfcProject")

def create_newIFC(ifcsource,path,filename):
    file_path=os.path.join(path,filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"DELETED EXISTING FILE:{filename}")
    with open(file_path,'w')as new_ifc_file:
        with open(ifcsource,'r')as ifcFile:
            for line in ifcFile:
                new_ifc_file.write(line)
                if line.strip()=="ENDSEC;":
                    break
                    ifcFile.close()
    print(f"New IFC file created: {filename}")


if __name__ =='__main__':

    #第一步应该是提取文件meta信息和project-site-building等信息
    #第二部，提取product-level info
    extracte_meta_info("D:\CimTestFile\SZW_RFJD_ARC_1F.ifc")
    pattern='''#\d+'''
    model=ifcopenshell.open("D:\CimTestFile\SZW_RFJD_ARC_1F.ifc")
    walls=model.by_type("Ifcwall")


    preprocess=modl_preprocess("D:\CimTestFile\SZW_RFJD_ARC_1F.ifc","Ifcwall")
    relationship=model_graph("D:\CimTestFile\SZW_RFJD_ARC_1F.ifc",preprocess)
    #(relationship)

    create_newIFC("D:\CimTestFile\SZW_RFJD_ARC_1F.ifc","D:\IFCOpenshell_python_version\Anaconda_ifc\IFC-source",
                  "output/newFile.ifc")

    #把所有相关位置和构形的id记录下来
    all_key=list(relationship.keys())
    all_values = [val for sublist in relationship.values() for val in sublist]
    new_ifclist=list(set(all_key+all_values))
    print(new_ifclist)
    with open("/IFC-source/output/newFile.ifc", 'a') as new_file:
        new_file.write("\n")
        new_file.write("DATA;\n")
        for i in range(0,len(new_ifclist)):
            instance=str(model.by_id(new_ifclist[i]))
            new_file.write(instance+'\n')
        new_file.write("\n")
        new_file.write("ENDSEC;\n")
        new_file.write("END-ISO-10303-21;")





    # for x in range(len(walls)):
    #     wall=walls[x]
    #     #预处理
    #     depth_1=re.findall(pattern,str(wall))
    #     graph_vertex1 = []
    #     for i in range(2,len(depth_1)):
    #         graph_vertex1.append(depth_1[i][1:])
    #     #print(f"第{x}个wall的位置和属性索引是：{graph_vertex1}")
    #     for j in range(len(graph_vertex1)):
    #         #print(build_instance_graph(model,int(graph_vertex1[j])))
    #
    #     print(f"第{x}个wall结束，还有{len(walls)-x-1}个")
    #     print("------------------------------------")
    # 把所有的id号存在一起提取出来，加上extracte_meta_info，组成*.ifc文件








