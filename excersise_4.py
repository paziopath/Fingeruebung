import networkx as nx
import os
import re
import spacy
import xml.etree.ElementTree as ET
import glob
import matplotlib.pyplot as plt

def graphs_show(x,y):
    """graph number 1"""
    g = nx.Graph()
    #[[id...],text,tag]
    #[rel,(from,to),color]
    
    for i in x:
        g.add_node(i[1])
    tags=[]
    for i in x:
        tags.append(i[2])
    
    color=[]
    for i in tags:
        if i == "PLACE":   
            color.append("b")
        elif i == "SPATIAL_ENTITY":
            color.append("r")
        elif i == "NONMOTION_EVENT":
            color.append("g")
        elif i == "PATH":
            color.append("m")
        elif i == "LOCATION":
            color.append("y")
            
    options = {"node_size": 100}

    edge=[]
    #labels=[]
    
    #print(labels)
    for i in y:
        p = []
        for j in x:
            for h in j[0]:
                if i[1][0]==h:
                    p.append(j[1]) #start
                    break
            for h in j[0]:
                if i[1][1] == h:
                    p.append(j[1])
                    break
            if len(p)==2:
                break
        edge.append([p,i[0],i[2]])
    edge_colors=[]

    for i in y:
        if i[2] == 1:
            edge_colors.append("g")
        elif i[2] == 2:
            edge_colors.append("r")
    
        
    for i in edge:
        if len(i[0]) < 2:
            g.add_edge(i[0][0],i[0][0])
        else:
            g.add_edge(i[0][0],i[0][1])
            #for j in y:
                #labels += [(j[0],"")]
    
    pos = nx.spring_layout(g)
    nx.draw(g, with_labels=True, font_weight='bold',node_color=color, cmap=plt.cm.Blues, **options, width=5,edge_color=edge_colors)
    #nx.draw_networkx_edge_labels(g, labels)
    plt.show()
    

def nodes(file):
    """given nodes"""
    n = [] #[[id...],text,tag]
    meta=[]
    nod= ["PLACE","SPATIAL_ENTITY","NONMOTION_EVENT", "PATH", "LOCATION"] 
    
    file_tree = ET.parse(file)
    file_root = file_tree.getroot()
    for i in file_root:
        for j in i:
            if j.tag == "METALINK":
                if j.attrib["toText"] not in meta:
                    meta.append([j.attrib["toText"],[[j.attrib["toID"],j.attrib["fromText"]]]])
                else:
                    for k in meta:
                        if k[0] == j.attrib["toText"]:
                            k[1].append([j.attrib["toID"],j.attrib["fromText"]])
                            break

    for i in file_root:
        for j in i:
            if j.tag in nod: # take possible node out of xml file       
                c = [j.tag, j.attrib]
                for k in meta:  # merge all totexts together
                    if j.attrib["text"] == k[0]:
                        for z in k[1]:
                            if j.attrib["id"] == z[0]: 
                                j.attrib["text"]=z[1]
                                break
                        c = [j.tag, j.attrib]
                        break    
            
                l=1
                for v in n:
                    if c[1]["text"] == v[1]:
                        v[0].append(c[1]["id"])
                        l=0
                if l==1:
                    n.append([[c[1]["id"]],c[1]["text"],c[0]])
                        
    return n


def edges_xml(file):
    """creates the edges for the nodes (qs-/o-links)"""
    
    link=[] #should both contain trigger + reltype
    
    file_tree = ET.parse(file)
    file_root = file_tree.getroot()
    for i in file_root:
        for j in i:
            if j.tag == "OLINK":
                link.append([j.attrib["relType"],(j.attrib["fromID"],j.attrib["toID"]), 1])
            elif j.tag == "QSLINK":
                link.append([j.attrib["relType"],(j.attrib["fromID"],j.attrib["toID"]), 2])

    return link #[rel,from,to],color]

    
def main():
    """visualizes Bicycles.xml and Highlights_of_the_Prado_Museum.xml"""

    while True:
        possibilities = []
        file1_input = input("Geben Sie ihren Ordner-Pfad mit Bicycles.xml an\n"
                               "z.B.: C:\\Users\\user_name\\...\\training\\Traning\\ANC\\WhereToJapan(here are the xml files): ")

        file1 = re.escape(file1_input)

        xml_file1 = glob.glob(os.path.join(file1, '*.xml'))
        
        for i in xml_file1:
           possibilities.append(i)

        graphs_show(nodes(possibilities[0]),edges_xml(possibilities[0]))
        graphs_show(nodes(possibilities[1]),edges_xml(possibilities[1]))
 
        
        
if __name__ == '__main__':
    main()
