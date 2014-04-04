import string
import random
import sys
import time
import re
import pdb

def DrawIPFile(inputfile):
    dipfile = {}
    with open(inputfile) as res:
        for line in res: 
            templine=line.decode('string_escape').strip("\"").strip()
            line_split=line.split('\t')#line_split[0]=dip_sip,line_split[1]=the attack fr
            dipsip=line_split[0].strip("\"")
            div_dipsip=dipsip.split(",")#div_dipsip[0]=dip,div_dipsip[1]=sip
            dip=div_dipsip[0].strip("\"")
        

            if dipfile.get(dip) is not None:
                dipfile.get(dip).append(templine)
            else:
                node_list = []
                node_list.append(templine)
                dipfile[dip] = node_list

    file_list=[]
    for (k,v) in dipfile.items():
        file_list.append(k)
        with open(k, 'wb') as file:
            res = list(set(v))
            att_content=[]
            usedRandomList=[]
            color_list=['olivedrab2','orange2','orangered2','orchid2','palegreen1','paleturquoise1','palevioletred1'] 
            i=0
            for alert in res:
                temp_alert=alert.decode('string_escape').strip("\"").strip("[").strip("]").strip()
                temp_div_alert=temp_alert.split("\t")#temp_div_alert[0]=dipsip,temp_div_alert[1]=the attack from sip to dip
                div_alert=str(temp_div_alert[0])
                dip_sip=div_alert.decode('string_escape').strip("\"").strip("[").strip("]").split(',')#dip_sip[0]=dip,

                temp_sip=dip_sip[1].decode('string_escape').strip("\"").strip("\'").strip()
                sip=temp_sip.decode('string_escape').strip("\"")
                label_value="label="+"\""+sip+"\""+";"

                
                random_color=color_list[(i%7)]
                i=i+1
                subgraph_color="color="+random_color+";"
                        
                random_char=string.join(random.sample(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o'], 7)).replace(" ","")
                random_num=random.randint(0,10000000)
                subgraph_name="subgraph"+" "+"cluster"+random_char+str(random_num)

                subgraph_style="style"+"="+"filled"+";"

                subgraph_node="node [style=filled,shape=plaintext];"
                attack=temp_div_alert[1].strip().strip("\"").split('->')
                ranksame=[]
                direction=[]
                att_time=[]
                label_list=[]
                time_label=[]
                time_name=[]
                timelabeldict={}
                finalranksame = []
                
                for each_attack in attack:
                    div_each_attack=each_attack.split(',')
                    random_char1=string.join(random.sample(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o'], 5)).replace(" ","")
                    random_num1=random.randint(0,1000)
                    while random_char1 in usedRandomList:
                        usedRandomList.append(random_char1)
                        random_char1 = string.join(random.sample(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o'], 5)).replace(" ","")
                    while random_num1 in usedRandomList:
                        usedRandomList.append(random_num1)
                        random_num1 = random.randint(0,1000)
                    time_mark=time.time()
                    att_name='%s'%(div_each_attack[1])+str(time_mark)+random_char1+str(random_num1) 

                    usedRandomList.append(random_char1)
                    usedRandomList.append(random_num1)

                    att_label="\""+att_name+"\""+"["+"label"+"="+"\""+each_attack[15:]+"\""+"]"
                    
                    label_list.append(att_label)
                    att_time.append(div_each_attack[0])
                     
                    
                    att_direction="\""+att_name+"\""+"->"+"\""+k+"\""+"\n"
                    direction.append(att_direction)

                    one_rank="{rank=same;"+"\""+'%s'%(div_each_attack[0])+"\""+";"+"\""+att_name+"\""+";"+"}"+"\n"
                    ranksame.append(one_rank)
                
                final_direction='\n'.join(direction)

                rev_time=list(set(att_time))
                sorted_time=sorted(rev_time)
                for each_time in sorted_time:

                    random_char3=string.join(random.sample(['p','q','r','s','t','u','v','w','x','y','z'], 5)).replace(" ","")
                    random_num3=random.randint(1000,10000)
                    
                    random_time_name=random_char3+str(random_num3)
                    one_time_label=random_time_name+"["+"label"+"="+"\""+each_time+"\""+"]"
                    timelabeldict[each_time] = random_time_name

                    time_label.append(one_time_label)  
                    time_name.append(random_time_name) 
                temptimeorder="->".join(time_name) #different time is connected by ->
                timeorder=temptimeorder+";\n"

                for r in ranksame:
                    regex = r"\"\d{2}/\d{2}-\d{2}:\d{2}:\d{2}\""
                    rersult = re.search(regex, r).group(0)
                    striptime =  rersult.strip("\"")
                    result,number = re.subn(regex, timelabeldict[striptime], r)
                    print r, result
                    finalranksame.append(result)
  
                rank="".join(list(finalranksame))
                label="\n".join(label_list)
                all_time_label="\n".join(time_label) 
                one_att_content=subgraph_name+"{"+"\n"+subgraph_node+"\n"+subgraph_style+"\n"+subgraph_color+"\n"+timeorder+all_time_label+"\n"+label+"\n"+rank+final_direction+label_value+"\n"+"}"
                att_content.append(one_att_content)

            final_content="\n".join(att_content)

            random_char2=string.join(random.sample(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o'], 7)).replace(" ","")
            random_num2=random.randint(0,1000)

            dip_subgraph_name=random_char2+str(random_num2)
            dip_subgraph_content="subgraph"+" "+"cluster"+dip_subgraph_name+"{"+"\n"+"node [color=red,shape=ellipse];"+"\n"+"\""+k+"\""+";"+"\n"+"}"

            filestring = """digraph G {\n%s\n%s\n}""" % (dip_subgraph_content,final_content)
            file.write(filestring)    
    return file_list        