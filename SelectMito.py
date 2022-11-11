import pandas as pd
import os
import sys
import numpy as np
pd.set_option("display.max_column",40)


def SeletMito(Mito_paf):
	f=pd.read_table(Mito_paf,header=None,sep=" ")
	f=f.groupby([0]).filter(lambda x: len(x)>=2)
	f=f.drop_duplicates([0,2,3],keep="first")
	f=f.sort_values([0,2,3])
	f[[0,2,3]].to_csv(Mito_paf+".bed",header=None,index=None,sep="\t")
	bedtools="bedtools merge -i %s -d 300 > %s"%(Mito_paf+".bed",Mito_paf+".bed.merge")
	os.system(bedtools)
	#print(f[0:10])
	#print(f.shape)
	fmerge=pd.read_table(Mito_paf+".bed.merge",header=None)
	fmerge=fmerge.groupby([0]).filter(lambda x: len(x)>=2)
	
	f=f.loc[f[0].isin(fmerge[0])]
	f.to_csv(Mito_paf+".selected.tsv",header=None,index=None,sep=" ")
	rm ="rm %s %s"%(Mito_paf+".bed", Mito_paf+".bed.merge")
	os.system(rm)

Mito_paf=sys.argv[1]

SeletMito(Mito_paf)
