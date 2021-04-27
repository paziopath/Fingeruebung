import os
import re
import spacy
import xml.etree.ElementTree as ET
import glob
import matplotlib as mlp
import matplotlib.pyplot as plt


def count(lst,ele):
    """counter for sum of each element in a (help func)"""
    c = 0
    for i in lst:
        if i == ele:
            c +=1        
    return c
 
def sentencelenght_graph(file):
    """makes a frequency-graph for the sentence length in a .xml file"""
    lengths =[] #length of each sentence
    counter = [] #
    
    x_lengths = [] #usage for graph
    y_counter = [] #usage for graph
    
    nlp = spacy.load("en_core_web_sm")
    plt.ylabel("Häufigkeit")
    plt.xlabel("Satzlänge")

    doc = nlp(file)

    for i in doc.sents:
        lengths.append(len(i)) 

    counter = sorted(lengths)

    for i in lengths:
        if i not in x_lengths:
            x_lengths.append(i)

    x_lengths = sorted(x_lengths)

    
    for i in x_lengths:
        y_counter.append(count(counter, i))
        
    
    plt.bar(x_lengths,y_counter)

    name_input = input("Geben Sie einen gewünschten Namen für die Bilddatei an: ")
    plt.savefig(name_input + ".png")

    
    

def sum_postags(lst):
    """takes a mtx, filters the tags out and determines the sum of each occuring pos tag """

    pos = {"ADJ":0,"ADP":0,"ADV":0, "AUX":0,"CONJ":0, "DET":0, "INTJ":0,"NOUN":0, "NUM":0, "PART":0, "PRON":0,"PROPN":0, "PUNCT":0, "SCONJ":0, "SYM":0, "VERB":0, "X":0, "SPACE":0, "CCONJ":0}
    
    for i in lst:
        pos[i[1]] +=1
                   
    return pos
            
            
def sum_things(file): #some things 
    """determines the sum of SpatialEntities, Places, Motions, Locations, Signals, QsLinks, OLinks"""

    to_be_counted = {"SPATIAL_ENTITY":0, "PLACE":0, "MOTION":0, "MOTION_SIGNAL":0,"SPATIAL_SIGNAL":0, "QSLINK":0, "OLINK":0}
    
    file_tree = ET.parse(file)
    file_root = file_tree.getroot()
    for i in file_root:
        for j in i:
            for k in to_be_counted.keys():
                if (j.tag == k):
                    to_be_counted[k] +=1
    return to_be_counted

def rel(file):
    """types of qslinks and how often they occur"""
    rel_types = {"IN":0, "OUT":0, "DC":0, "EC":0,"PO":0, "TPP":0, "ITPP":0, "NTPP":0, "INTPP":0, "EQ":0}
    
    file_tree = ET.parse(file)
    file_root = file_tree.getroot()
    for i in file_root:
        for j in i:
            for k in rel_types.keys():
                if j.tag == "QSLINK":
                    if (j.attrib["relType"] == k):
                        rel_types[k] +=1
    return rel_types

def motion_verbs(file):
    """gives the 5th most occuring motion_verbs in a .xml file"""
    verbs = {}
    verbs_sorted = {}
    verbs_final = []
    file_tree = ET.parse(file)
    file_root = file_tree.getroot()
    for i in file_root:
        for j in i:
            if j.tag == "MOTION":
                verbs.update({j.attrib["text"] : 0})

    for i in file_root:
        for j in i:
            for k in verbs.keys():
                if j.tag == "MOTION":
                    if(j.attrib["text"]==k):
                        verbs[k] +=1

    by_values = sorted(verbs.values())

    for i in by_values:
        for j in verbs.keys():
            if verbs[j] == i:
                verbs_sorted[j] = verbs[j]
                
    for i,j in verbs_sorted.items():
        verbs_list = [i,j]
        verbs_final.append(verbs_list)

    verbs_final = verbs_final[-5:]
    verbs_final = verbs_final[::-1]

    return verbs_final

def which_prep(file):
    """gives the trigger-words with the number of occurences"""
    spatial = []
    qs = []
    file_tree = ET.parse(file)
    file_root = file_tree.getroot()
    for i in file_root:
        for j in i:
            if j.tag == "SPATIAL_SIGNAL":
                spatial.append([j.attrib["id"], j.attrib["text"], 0])
            elif j.tag == "QSLINK":
                qs.append([j.attrib["trigger"],j.attrib["id"]])

    for i in range(0, len(spatial)):
        for j in range(0, len(qs)):
            if spatial[i][0] == qs[j][0]:
                spatial[i][2] +=1
                spatial[i].append(qs[j][1])

    return spatial


def token(x):
    """lists  all pos tags (help func)"""
    list_of_things = []
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(x)
    for token in doc:
        list_of_things.append([token.text, token.pos_, token.tag_])

    return list_of_things

def read_xml(file):
    """ takes an .xml file and reads it"""

    final_text=""    
    
    file_tree = ET.parse(file)
    file_root = file_tree.getroot()
    for i in file_root:
        if i.tag == "TEXT":
            final_text = final_text + i.text    
    return final_text

def main():
    """tool for reading a xml file"""

    while True:
        possibilities = []
        bloop = []
        file_directory_input = input("Geben Sie ihren Ordner-Pfad mit den XML-Dateien an\n"
                               "z.B.: C:\\Users\\user_name\\...\\training\\Traning\\ANC\\WhereToJapan(here are the xml files): " ) #asks for the path of a folder with xml files

    
        file_directory = re.escape(file_directory_input) #changes \ --> \\ so unicode error is avoided
        
        is_dir = os.path.isdir(file_directory)
        xml_file = glob.glob(os.path.join(file_directory, '*.xml'))

        for i in xml_file:
           possibilities.append(i)
        
        for j in possibilities:
            bloop.append(read_xml(j)) #list with every .xml file in given directory

        
        if is_dir == True:
        
            tokens=[]
            for h in range(0,len(bloop)):
                tokens.append(sum_postags(token(bloop[h]))) #1st subexcersice: how often do which pos tags occur in the .xml file?
            
            how_many=[]
            for h in range(0,len(possibilities)):
                how_many.append(sum_things(possibilities[h])) #2nd subexcersice: how many spatialentities...exist in the .xml file?

            how_many_qs=[]
            for h in range(0,len(possibilities)):
                how_many_qs.append(rel(possibilities[h])) #3rd subexcersice: how often do which qslinks occur?

            preps=[]
            for h in range(0,len(possibilities)):
                preps.append(which_prep(possibilities[h])) #5th subexcersice: how often do which qslinks occur?

            moverb=[]
            for h in range(0,len(possibilities)):
                moverb.append(motion_verbs(possibilities[h])) #6th subexcersice: 5 most occuring motion verbs?
                
            for h in range(0,len(bloop)):
                sen_le = sentencelenght_graph(bloop[h]) #4th subexcersice: give the distribution of the frequency of sentence lengths

            
            ask_for_name = input("Wie soll die Datei mit den Daten heißen?: ")
            file_with_data = open(ask_for_name + ".txt", "w+")

            data = [tokens,how_many,how_many_qs,preps,moverb] #len 5

            file_with_data.write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
            file_with_data.write("Die Daten sind jeweils der Reihenfolge der Ordner nach angeordnet\n")
            file_with_data.write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
            file_with_data.write("\n")
            for i in range(0, len(data)):
                v = len(data[i])
                for k in range(0,v):
                    file_with_data.write(str(data[i][k]) + "\n")
                file_with_data.write("-----------------------------------------------------------------------------------%d\r\n" %(i+1))
                if i+1 == 3:
                    file_with_data.write("Zum Verständnis: Es handelt sich hierbei um eine Liste, in der zuerst die Spatial-id, die den QS-Link triggert\n")
                    file_with_data.write("danach wird das Trigger-Wort aufgelistet, wie oft es getriggert hat und welche QS-Links betroffen sind\n")
                    file_with_data.write("\n")
           
            file_with_data.close()
            
            print("")
            print("-----------------------------------------------------------------------------------------------------")
            print("Sie finden die Bilder/.txt aller .xml Dateien, im selben Ordner gespeichert, indem das Programm liegt")
            print("-----------------------------------------------------------------------------------------------------")
            print("")

            #last thing: distribute the data for each xml file, i could use the matrix and always take the data
        else:
            print("")
            print("Die Eingabe war falsch. Es sind nur gültige Pfade erlaubt")
            print("")
            
        
if __name__ == '__main__':
    main()
