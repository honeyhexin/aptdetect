import string
import re
import random

def DrawTimeFile(inputfile):
    datefile = {}
    date_pattern=re.compile(r'\d{2}/\d{2}')
    time_pattern=re.compile(r'\d{2}:\d{2}:\d{2}')
    with open(inputfile) as res:
        for line in res:
            line_split = line.split('\t')#line_split[0]=time,line_split[1]=A->B

            temptime = line_split[0].strip("\"")#line_spilt[0]=time
            matchdate=date_pattern.search(temptime)#match the date from time
            tempdate=matchdate.group() 
            date=string.replace(tempdate,"/","-")#08/02 is transformed into 08-02

            temp_pre_con=line_split[1].decode('string_escape').strip("\"")

            pre_con=temp_pre_con.split('->')#pre_com[0]=pre,pre_con[1]=con
            
            pre=pre_con[0].split(',')#pre[0]=time,pre[1]=sigid,pre[2]=sigrev,pre[3]=description,pre[4]=protocol,pre[5]=sip,pre[6]=sport,pre[7]=dip,pre[8]=dip,
            #matchtime=time_pattern.search(pre[0])
            #pre_time=matchtime.group()
            pre_time=string.replace(pre[0],"/","-")
            prevalue=[pre_time,pre[3],pre[5],pre[7]]#prevalue=[time,discription,sip,dip]
            prevalue_str=','.join(prevalue)#list is transformed into str 

            con=pre_con[1].split(',')#con[0]=time,con[1]=sigid,con[2]=sigrev,con[3]=description,con[4]=protocol,con[5]=sip,con[6]=sport,con[7]=dip,con[8]=dip,
            #matchtime=time_pattern.search(con[0])
            #con_time=matchtime.group()
            con_time=string.replace(con[0],"/","-")
            convalue=[con_time,con[3],con[5],con[7]]
            convalue_str=','.join(convalue)

            value=prevalue_str+'->'+convalue_str#value=pre->con;

            v2 = string.replace(value, "\"", "")
            store = string.replace(v2, "->", "#")
            v3 = string.replace(store, "-", "_")
            back  = string.replace(v3, "#", "->")
            v4 = string.replace(back, " ", "_")      
            if datefile.get(date) is not None:
                datefile.get(date).append(v4)
            else:
                node_list = []
                node_list.append(v4)
                datefile[date] = node_list

    file_list=[]
    for (k,v) in datefile.items():
        file_list.append(k)
        with open(k, 'wb') as file:
            att_value=[]
            att_time=[]
            ranksame=[]
            after_sorted=[]
            label_list=[]
            res = list(set(v))
            for alert in res:
                split_alert=alert.split('->')#split_alert[0]=pre,split_alert[1]=con
                pre=split_alert[0].split(',')#pre[0]=time,pre[1]=discription,pre[2]=sip,pre[3]=dip
                con=split_alert[1].split(',')#con[0]=time,con[1]=discription,con[2]=sip,con[3]=dip

                random_char1=string.join(random.sample(['a','b','c','d','e','f','g','h','i','j'], 5)).replace(" ","")
                random_num1=random.randint(0,10000)
                pre_name='%s'%(pre[1])+random_char1+str(random_num1)
                random_char2=string.join(random.sample(['a','b','c','d','e','f','g','h','i','j'], 5)).replace(" ","")
                random_num2=random.randint(0,10000)
                con_name='%s'%(con[1])+random_char2+str(random_num2)
                
                pre_att='%s'%(pre[1])+random_char1+str(random_num1)+"["+"label"+"="+"\""+"%s"%(pre[1])+"\\n"+"sip:"+'%s'%(pre[2])+"\\n"+"dip:"+'%s'%(pre[3])+"\""+"]"
                con_att='%s'%(con[1])+random_char2+str(random_num2)+"["+"label"+"="+"\""+"%s"%(con[1])+"\\n"+"sip:"+'%s'%(con[2])+"\\n"+"dip:"+'%s'%(con[3])+"\""+"]"
                
                label_list.append(pre_att)
                label_list.append(con_att)

                pre_con_att='%s'%(pre_name)+"->"+'%s'%(con_name)
                att_value.append(pre_con_att)# pre time is append into the att_time list

                att_time.append(pre[0])
                att_time.append(con[0])
                #one_rank="{rank=same;"+"\""+pre[0]+"\""+";"+"\""+pre[1]+','+pre[2]+','+pre[3]+','+"\""+";"+"\""+con[0]+','+con[1]+','+con[2]+"\""+"}"+'\n' 
                one_rank="{rank=same;"+"\""+'%s'%(pre[0])+"\""+";"+'%s'%(pre_name)+";"+"}"+"\n"
                two_rank="{rank=same;"+"\""+'%s'%(con[0])+"\""+";"+'%s'%(con_name)+";"+"}"+"\n"
                ranksame.append(one_rank)
                ranksame.append(two_rank)

            rev_time=list(set(att_time))
            sorted_time=sorted(rev_time)
            for time in sorted_time:
                after_sorted_time="\""+time+"\""
                after_sorted.append(after_sorted_time)     
            temptimeorder="->".join(after_sorted) #different time is connected by ->
            timeorder=temptimeorder+";\n"

            label="\n".join(label_list)
            rank="".join(list(ranksame)) 
            content = ";\n".join(att_value)
            node_shape="node[shape=plaintext];"+"\n"


            filestring = """digraph G {\n%s\n%s\n%s\n%s\n%s\n}""" % (node_shape,timeorder,label,rank,content)
            file.write(filestring)
    return file_list

