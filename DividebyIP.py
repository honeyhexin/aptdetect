from mrjob.job import MRJob
import re
import string
import traceback
import sys
import pickle


class DividebyIP(MRJob):
    def mapper(self,_,line):
        
        line=line.strip()
        div_line=line.split('\t')#div_line[0]=dip,div_line[1]=the attack to the dip
        dip=div_line[0].strip("\"").decode('string_escape')
        tempalert=div_line[1].strip("\"").decode('string_escape')
        alert_att=tempalert.split(',')#alert_att[0]=time,alert_att[1]=sigid,alert_att[2]=sigrev,alert_att[3]=discription,alert_att[4]=protocol,alert_att[5]=sip,alert_att[6]=sport,alert_att[7]=dip,alert_att[8]=dport
        dip_alert_att=alert_att[0]+","+alert_att[3].strip("\"").decode('string_escape')
        dip_sip=dip+","+alert_att[5]
        sys.stderr.write("\n dip_alert_att"+dip_alert_att+"\n")
        yield(dip_sip,dip_alert_att)
        

    def reducer(self,dip_sip,dip_alert): 

        final_dip_sip=dip_sip
        temp_dip_alert=list(dip_alert)
        #yield(final_dip,pickle.dumps(final_dip_alert))
        #final_dip_alert=list(temp_dip_alert.strip().strip('\"').strip('[').strip(']'))
        final_dip_alert='->'.join(temp_dip_alert)
        yield(final_dip_sip,final_dip_alert)

if __name__=='__main__':
    DividebyIP.run()   	