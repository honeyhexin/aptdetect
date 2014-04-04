#!/usr/bin/env python
#encoding:utf-8 

from mrjob.job import MRJob
import sys
import string
import re
import traceback
import pickle
class DividebyTime(MRJob):
    def mapper(self,_,line):
        try:
            alert_set=str(line).strip('\"').decode('string_escape')
            sys.stderr.write("\nline "+str(alert_set)+"\n")
            alert_set_split=alert_set.split('\t')#line[0]=alert,line[1]=alertset
            alert=alert_set_split[0].strip('\"').decode('string_escape')
            #date_pattern=re.compile(r'\d{2}/\d{2}')
            div_alert=str(alert).split(',')#div_alert[0]=time,div_alert[1]=sigid,div_alert[2]=sigrev,div_alert[3]=description,div_alert[4]=protocol,div_alert[5]=dip,div_alert[6]=dport,div_alert[7]=sip,div_alert[8]=sport
            #tempdate=date_pattern.search(div_alert[0])
            sys.stderr.write("\n alert_set_split[1] "+alert_set_split[1].strip("\"")+"\n")

            alert_list = pickle.loads(alert_set_split[1].strip("\""))
            #sys.stderr.write("\nalert_list "+str(alert_list)+"\n")
            date=div_alert[0]
            yield(date,alert_set)
        except Exception,e:
            sys.stderr.write(str(traceback.print_exc()))    

    def reducer(self,date,date_alert):
    	try:
            # sys.stderr.write("\ndate "+date+"\n"+"\ndate_alert "+str(list(date_alert)) + "\n")
            for each_list_set in date_alert:
                splitresult=each_list_set.split('\t')
                #sys.stderr.write("\nsplitresult[1] "+str(splitresult)+"\n")
                alert_list = pickle.loads(splitresult[1].strip("\""))
                # sys.stderr.write("\n alertList: "+str(alert_list) + "\n");
                for each_alert in alert_list:
                    yield(date, "%s->%s"%(splitresult[0].strip("\""),each_alert.strip("\"")))
        except Exception,e:
            sys.stderr.write(str(traceback.print_exc()))
        

	
if __name__=='__main__':
    DividebyTime.run()




