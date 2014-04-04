#!/usr/bin/env python
#encoding:utf-8 

from mrjob.job import MRJob
import sys
import string
import pickle
import datetime
import traceback

class AggreAlerts(MRJob):
    def correlation_judge(self,a,b):
        try:
            with open('knowledgebase.pickle','rb') as f:
                knowbase=pickle.load(f)
                a=a.split(',')#a[0]=time,a[1]=sigid,a[2]=sigrev.a[3]=discription,a[4]=protocol,a[5]=sip,a[6]=sport,a[7]=dip,a[8]=dport
                b=b.split(',')#b[0]=time,b[1]=sigid,b[2]=sigrev.b[3]=discription,b[4]=protocol,b[5]=sip,b[6]=sport,b[7]=dip,b[8]=dport
                a_time=datetime.datetime.strptime(a[0],"%m/%d-%H:%M:%S")
                b_time=datetime.datetime.strptime(b[0],"%m/%d-%H:%M:%S")
                if(a_time<b_time and a[7]==b[7] and a[5]==b[5] and int(b[1]) in knowbase[str(a[1])]['con']):
                    return True
                else:
                    return False
        except Exception,e:
            pass
            # sys.stderr.write(str(traceback.print_exc()))

    def mapper(self,_,line):
        line=line.strip()
        line=line.split('\t')#line[0]=dip,line[1]=alert
        dip=line[0].strip('\"').decode('string_escape')
        alert=line[1].strip('\"').decode('string_escape')
        yield(dip,alert)

    def reducer(self,dip,alert):
        alert_list = list(alert)
        sys.stderr.write("\n dip "+dip+"\n alert_list "+str(alert_list)+"\n")
        for a_alert in alert_list:
                for b_alert in alert_list:
                    if(a_alert==b_alert):
                        continue
                    else:
                        aTob=self.correlation_judge(a_alert,b_alert)
                        bToa=self.correlation_judge(b_alert,a_alert)
                        if(aTob==True):
                            yield(a_alert.decode('string_escape'),b_alert.decode('string_escape'))
                        else:
                            continue    
                                

if __name__=='__main__':
    AggreAlerts.run()
        
        
