是带buffer的缓冲流
        Map<Integer,List<Integer>> reference =new HashMap<>();
        Reader reader=null;
        try{
            reader=new FileReader(filePath);
        }catch (FileNotFoundException e)
        {
            e.printStackTrace();
        }
        BufferedReader br=new BufferedReader(reader);
        String line;
        try {
            boolean begin_instance = false;
            while((line=br.readLine())!=null)
            {
                if (!begin_instance) {
                    if (line.trim().equals("DATA;")) {
                        begin_instance = true;

                    }
                    continue;  // 跳过 "DATA;" 行之前的内容
                }
                List<Integer> ids =IFCGraph.extractIds(line);
                if (ids.size()>1)
                {
                    int node=ids.get(0);
                    List<Integer>node_children=ids.subList(1,ids.size());
                    reference.put(node,node_children);
                }


            }
        }catch (IOException e)
        {
            e.printStackTrace();
        }
        return reference;





    }
    private static List<Integer> extractIds(String text) {
        List<Integer> ids = new ArrayList<>();
        Pattern pattern = Pattern.compile("#\\d+");
        Matcher matcher = pattern.matcher(text);

        while (matcher.find()) {
            String match = matcher.group();
            // 将匹配到的字符串中的数字部分转化为整数并添加到列表
            int id = Integer.parseInt(match.substring(1));

            ids.add(id);
        }

        return ids;
    }
    private static void processIds(Map<Integer, List<Integer>> ids, String filePath, Map<Integer, Object> graph) {
        for (Map.Entry<Integer, List<Integer>> entry : ids.entrySet()) {
            Integer node = entry.getKey();
            List<Integer> nodeChildren = entry.getValue();

            if (graph == null) {
                graph = new HashMap<>();
            }

            graph.put(node, nodeChildren);
            //System.out.println(graph);
            for (Integer child : nodeChildren) {
                String childLocation = '#' + child.toString();
                String matchLine = null;

                try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
                    String line;

                    while ((line = br.readLine()) != null) {
                        if (line.trim().startsWith(childLocation)) {
                            matchLine = line;
                            List<Integer> subIds = extractIds(matchLine);

                            if (subIds.size() >= 2)//递归终止条件需要添加
                            {
                                // map存储引用关系{child, child_Reference}
                                Map<Integer, List<Integer>> subsReference = new HashMap<>();
                                subsReference.put(subIds.get(0), subIds.subList(1, subIds.size()));

                                // 递归调用
                                processIds(subsReference, filePath, graph);
                            }

                            break;
                        }
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }
}
