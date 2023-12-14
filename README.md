# todo：
1. IFC转为MESH,计算 Circularity、Convexity、Fractality、cohesion、Dispersion指标
2. 文件分割慢，润色两个部分：  
   * ~~考虑用mapreduce对ifc文件分成product-level方法~~
   * I/O量，减少文件打开次数
   * 递归函数优化，减少没必要的检索。
3. 增加对material、color属性的存储
4. 优化write_file程序的输入参数
5. 考虑如何用并行计算加快处理。
# done：
~~1. IFC信息提取位置和构形数据,meta-data,并且提取空间组织关系实体。~~   
~~2. 提取的IFC文件可以在bimvision打开~~  
~~3. 学习occtPython,draw an boundingbox.~~  
~~4. 测试多个instance提取~~      
~~5. 多个构件的包围盒加载显示~~  
~~6, 体积、面积基于opencascade完成~~  

测试总结：
2MB(2000KB)的建筑文件，2.4w行文本记录：提取出来200+IfcWall，文件大小290kb，压缩为15%，花费20分钟，大概3000行记录。

![image](https://github.com/deliciousteas/IFC_info_extraction/assets/107855849/6dfb11a4-3195-426c-b24e-6c9d2dfa7bb5)

![img.png](img.png)
![img_1.png](img_1.png)