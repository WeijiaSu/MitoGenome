import pandas as pd
import os
import sys
pd.set_option("display.max_column",40)

def map_ratio(sub_f):
  r_len=int(list(sub_f["ReadLen"])[0])
  l=zip(sub_f["ReadStart"],sub_f["ReadEnd"])
  a=np.array([0]*r_len)
  for i in l:
    a[i[0]:i[1]+1]=1
  return list(a).count(1)


def getAlig(file_genome,file_TE):
	f1=pd.read_table(file_genome,header=None,sep=" ")
	print(len(set(f1[0])))
	f2=pd.read_table(file_TE,header=None,sep=" ")
	print(len(set(f2[0])))
	f2=f2.loc[f2[0].isin(f1[0])]
	f1=f1[range(0,12)]
	f2=f2[range(0,12)]
	f1.columns=["ReadName","ReadLen","Readref_s","Readref_e","RefStrand","RefName","RefLen","Ref_s","Ref_e","Ref_match","Ref_alig","Ref_score"]

	f2.columns=["ReadName","ReadLen","Readte_s","Readte_e","TEStrand","TEName","TELen","TE_s","TE_e","TE_match","TE_alig","TE_score"]

	f=f1.merge(f2,on=["ReadName","ReadLen"],how="inner")
	f=f.loc[(f["Readref_e"]<f["Readte_s"]+100) | (f["Readref_s"]>f["Readte_e"]-100)]
	f=f.sort_values(["ReadName","Readte_s","Readte_e"])
	r=f.drop_duplicates(["ReadName"],keep="first")
	r_g=r.groupby(["TEName"],as_index=False).count().sort_values(["ReadName"],ascending=[False])
	print(f[0:50])
	#print(r_g[0:10])
	#print(r_g.shape)
	#print(f[0:20])
	#print(f.shape)
	#print(r.shape)
	#print(len(set(f["ReadName"])))
	
file_genome=sys.argv[1]
file_TE=sys.argv[2]

getAlig(file_genome,file_TE)
