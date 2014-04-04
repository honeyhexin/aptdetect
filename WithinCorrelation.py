#!/usr/bin/env python
#encoding:utf-8 

from mrjob.job import MRJob
import sys
import string
import pickle

class WithinCorrelation(MRJob):
    def mapper(self,_,line):
        line=line.strip()
        line=line.split('\t')
        a_alert=line[0].strip('\"').decode('string_escape')
        b_alert=line[1].strip('\"').decode('string_escape')
        yield(a_alert,b_alert)

    def reducer(self,a,b):
        a_alert=a.decode('string_escape')
        a_alert_set=list(b)
        yield(a_alert,pickle.dumps(a_alert_set))

if __name__=='__main__':
    WithinCorrelation.run()
