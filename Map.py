import pandas as pd
import os
import sys
import numpy as np
from Bio import SeqIO
pd.set_option("display.max_column",40)




def GetReads(dire,Accession):
	reads=dire+Accession+".fastq"
	records=list(SeqIO.parse(reads,"fastq"))
	NanoStat="NanoStat --fastq %s -n %s"%(reads,Accession+".NanoStat")
	os.system(NanoStat)
	return len(records)


def GetMap(Accession):
	f=pd.read_table(Accession+".fastq_chrM.fa.paf",header=None,sep=" ")
	f=f.drop_duplicates([0],keep="first")
	return f.shape[0]


dire=sys.argv[1]
Accession=sys.argv[2]

nReads=GetReads(dire,Accession)
Mapped=GetMap(Accession)
ratio=round(Mapped/nReads*100,2)
print(Accession+" "+str(nReads)+" " + str(Mapped)+" "+ str(ratio))
