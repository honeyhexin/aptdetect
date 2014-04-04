from mrhob import *
from AggreAlerts import *
from WithinCorrelation import *
from DividebyTime import *
from DividebyIP import *
from DrawTimeFile import *
from DrawIPFile import *
import pdb
import shlex
import subprocess

def runJob(jobname, inputfile, outputfile, errfile,otherfile):
    if otherfile is not None:
        mr_job = jobname(args=["--file",otherfile,inputfile])
    else:    
        mr_job = jobname(args=[inputfile])
    f = open(outputfile, "wb")
    ferr = open(errfile, "wb")
    mr_job.sandbox(stdout=f, stderr=ferr)
    with mr_job.make_runner() as runner:
        runner.run()
        for line in runner.stream_output():
            key, value = mr_job.parse_output_line(line)
            f.write('%s\t%s\n'%(key,value.encode('string-escape')))
    return outputfile   

def runMrhob(inputfile, outputfile):
    return runJob(MR_Eliminate_redundant, inputfile, outputfile, 'defaulterr.csv',None)
def runAggreAlerts(inputfile,outputfile):
    return runJob(AggreAlerts, inputfile, outputfile, 'defaulterr.csv',"knowledgebase.pickle")  
def runWithcorrelation(inputfile,outputfile):
    return runJob(WithinCorrelation, inputfile, outputfile, 'defaulterr.csv',None)
def runDividebyIP(inputfile,outputfile):
    return runJob(DividebyIP, inputfile, outputfile, 'defaulterr.csv',None)
def runDividebyTime(inputfile,outputfile):
    return runJob(DividebyTime, inputfile, outputfile, 'defaulterr.csv',None)
     
def DrawFile(filename):
    command_line="dot -Tjpeg "+filename+" -o "+filename+".jpeg"
    args=shlex.split(command_line)
    p=subprocess.Popen(args)


if __name__=="__main__":
    mrhob_output =runMrhob("test400.csv", "mrhob_result")
    AggreAlerts_output=runAggreAlerts("mrhob_result","Aggre_result")
    Withcorrelation_output=runWithcorrelation("Aggre_result","With_result")
    DividebyIP_output=runDividebyIP("mrhob_result","DividebyIP_result")
    DividebyTime_ouput=runDividebyTime("With_result","DividebyTime_result")
    Drawtime_output=DrawTimeFile("DividebyTime_result")
    DrawIP_output=DrawIPFile("DividebyIP_result")
    for each_time in Drawtime_output:
        DrawFile(each_time)
    for each_IP in DrawIP_output:
        DrawFile(each_IP)    