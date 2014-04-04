#!/usr/bin/env python
#encoding:utf-8

from mrjob.job import MRJob
import sys
import string
import datetime
import re



class MR_Eliminate_redundant(MRJob):

    def mapper(self,_,line):
        line=line.strip()
        time_pattern=re.compile(r'\d{2}/\d{2}-\d{2}:\d{2}:\d{2}')

        try:
            line=line.split(',')#line[0]='08/04-18:16:23.468455',line[1]=sigid,line[2]=sigrev,line[3]='PROTOCOL-ICMP PING BSDtype',line[4]='ICMP',line[5]=sip,line[6]=sport,line[7]=dip,line[8]=dport
            temptime=time_pattern.search(line[0])
            line[0]=temptime.group()
            dip='%s'%line[7]
            alert='%s,%s,%s,%s,%s,%s,%s,%s,%s'%(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8])

            yield(dip,alert)#alert='08/04-18:16:23,368,10,"PROTOCOL-ICMP PING BSDtype",ICMP,192.168.103.55,dport,192.168.102.2,sport '

        except Exception,e:
            pass

    def combiner(self,dip,alert):
        temp_alert_list = list(each_alert for each_alert in alert)
        alert_list=list(set(temp_alert_list))

        sys.stderr.write('\n In Combiner alert list is %s\n' % str(alert_list))
        # print alert_list
        try:
            for a_alert in alert_list:
                for b_alert in alert_list:
                    if(a_alert==b_alert):
                        continue
                    else:
                        a=a_alert.split(',')#a[0]='08/04-18:16:23',a[1]=sigid,a[2]=sigrev,a[3]='PROTOCOL-ICMP PING BSDtype',a[4]='ICMP',a[5]=sip,a[6]=sport,a[7]=dip,a[8]=dport
                        b=b_alert.split(',')#b[0]='08/04-18:16:23',b[1]=sigid,b[2]=sigrev,b[3]='PROTOCOL-ICMP PING BSDtype',b[4]='ICMP',b[5]=sip,b[6]=sport,b[7]=dip,b[8]=dport
                        a_time=datetime.datetime.strptime(a[0],"%m/%d-%H:%M:%S")
                        b_time=datetime.datetime.strptime(b[0],"%m/%d-%H:%M:%S")
                        if(a_time > b_time):
                            interval_days=(a_time - b_time).days
                            interval_sec=(a_time - b_time).seconds
                        elif(a_time < b_time):
                            interval_days=(b_time - a_time).days
                            interval_sec=(b_time - a_time).seconds
                        else:
                            interval_days=0
                            interval_sec=0

                        if(interval_days==0 and interval_sec <=600 and a[5]==b[5] and a[1]==b[1]):

                            alert_list.remove(b_alert)
                        else:
                            continue
        except Exception,e:
            print str(e)
        for alert in alert_list:
            yield(dip, '%s' % alert)

    def reducer(self,dip,alert):
        temp_alert_list = list(each_alert for each_alert in alert)
        alert_list=list(set(temp_alert_list))
        sys.stderr.write('\n In Reducer alert list is %s\n' % str(alert_list))
        # print alert_list
        try:
            for a_alert in alert_list:
                for b_alert in alert_list:
                    if(a_alert==b_alert):
                        continue
                    else:
                        a=a_alert.split(',')#a[0]='08/04-18:16:23',a[1]=sigid,a[2]=sigrev,a[3]='PROTOCOL-ICMP PING BSDtype',a[4]='ICMP',a[5]=dip,a[6]=dport,a[7]=sip,a[8]=sport
                        b=b_alert.split(',')#b[0]='08/04-18:16:23',b[1]=sigid,b[2]=sigrev,b[3]='PROTOCOL-ICMP PING BSDtype',b[4]='ICMP',b[5]=dip,b[6]=dport,b[7]=sip,b[8]=sport
                        a_time=datetime.datetime.strptime(a[0],"%m/%d-%H:%M:%S")
                        b_time=datetime.datetime.strptime(b[0],"%m/%d-%H:%M:%S")
                        if(a_time > b_time):
                            interval_days=(a_time - b_time).days
                            interval_sec=(a_time - b_time).seconds
                        elif(a_time < b_time):
                            interval_days=(b_time - a_time).days
                            interval_sec=(b_time - a_time).seconds
                        else:
                            interval_days=0
                            interval_sec=0
                        if(interval_days==0 and interval_sec <=600 and a[7]==b[7] and a[1]==b[1]):
                            alert_list.remove(b_alert)
                        else:
                            continue
        except Exception,e:
            sys.stderr.write(str(e))
        for alert in alert_list:
            yield(dip, '%s' % alert)
"""
    def steps(self):
        return [self.mr(mapper=self.mapper,
                        combiner=self.combiner,
                        reducer=self.reducer)]
"""

