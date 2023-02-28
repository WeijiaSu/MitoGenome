import pandas as pd
import os
import sys
import numpy as np
from Bio import SeqIO
pd.set_option("display.max_column",40)



Name=sys.argv[3]
def GetReads(reads):
	records=list(SeqIO.parse(reads,"fastq"))
	NanoStat="NanoStat --fastq %s -n %s"%(reads,Name+".NanoStat")
	os.system(NanoStat)
	return len(records)


def GetMap(paf):
	f=pd.read_table(paf,header=None,sep=" ")
	f=f.drop_duplicates([0],keep="first")
	return f.shape[0]


reads=sys.argv[1]
paf=sys.argv[2]

nReads=GetReads(reads)
Mapped=GetMap(paf)
ratio=round(Mapped/nReads*100,2)
print(Name+" "+str(nReads)+" " + str(Mapped)+" "+ str(ratio))
