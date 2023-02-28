import pandas as pd
import os
import sys
import numpy as np
pd.set_option("display.max_column",40)




def map_ratio(sub_f):
	r_len=int(list(sub_f["ReadLen"])[0])
	l1=zip(sub_f["Readref_s"],sub_f["Readref_e"])
	l2=zip(sub_f["Readte_s"],sub_f["Readte_e"])
	l=list(l1)+list(l2)
	a=np.array([0]*r_len)
	for i in l:
		a[int(i[0]):int(i[1])+1]=1
	return list(a).count(1)/r_len*100

name=sys.argv[3]

def getAlig(file_genome,file_TE):
	f1=pd.read_table(file_genome,header=None,sep=" ")
	f1=f1.loc[f1["RefName"]=="chrM"]
	f2=pd.read_table(file_TE,header=None,sep=" ")
	f2=f2.loc[f2[0].isin(f1[0])]
	f1=f1[range(0,12)]
	f2=f2[range(0,12)]
	f1.columns=["ReadName","ReadLen","Readref_s","Readref_e","RefStrand","RefName","RefLen","Ref_s","Ref_e","Ref_match","Ref_alig","Ref_score"]

	f2.columns=["ReadName","ReadLen","Readte_s","Readte_e","TEStrand","TEName","TELen","TE_s","TE_e","TE_match","TE_alig","TE_score"]

	f=f1.merge(f2,on=["ReadName","ReadLen"],how="inner")
	fs=f.loc[(f["Readref_e"]<f["Readte_s"]+100) | (f["Readref_s"]>f["Readte_e"]-100)]
	fs=fs.sort_values(["ReadName","Readte_s","Readte_e"])
	f["m"]=0
	f=f.loc[f["ReadName"].isin(list(fs["ReadName"]))]
	r=f.drop_duplicates(["ReadName"],keep="first")
	
	for read in list(r["ReadName"]):
		sub=f.loc[f["ReadName"]==read]
		m=map_ratio(sub)
		f.loc[f["ReadName"]==read,"m"]=m
		
	f=f.loc[f["m"]>=90]
	#f=f.groupby(["ReadName"]).filter(lambda x: len(x)>=2)
	fs2=f.loc[(f["TE_s"]<=100) & (f["TE_e"]>=f["TELen"]-100) ]
	f=f.loc[f["ReadName"].isin(list(fs2["ReadName"]))]
	f.to_csv(name+"intTE.tsv",header=None,index=None,sep="\t")
	rm ="rm %s"%(file_genome)
	os.system(rm)

file_genome=sys.argv[1]
file_TE=sys.argv[2]

getAlig(file_genome,file_TE)
