import cellxgene_census
import numpy as np
import pandas as pd
import scanpy as sc
import os
import glob
import joblib

from multiprocessing import Pool
import time

os.makedirs("01data/",exist_ok=True)
N=10000

def run(argv):
    name, start_l,end_l, id_list=argv
    save_filename="01data/{}.{:08d}-{:08d}.jbl".format(name,start_l,end_l)
    target_var=pd.read_csv("00data/"+name+".var.tsv",sep="\t", index_col=0)
    target_gene_ids = target_var["soma_joinid"].to_numpy()
    if os.path.isfile(save_filename):
        print("[skip]",save_filename)
    else:
        census=None
        try:
            census = cellxgene_census.open_soma(census_version="2023-12-15")
        except:
            print('Error onece cellxgene open') 
            time.sleep(10)
            census=None
        if census is None:
            # retry
            census = cellxgene_census.open_soma(census_version="2023-12-15")
        save_filename

        try:
            target_adata = cellxgene_census.get_anndata(
                census,
                organism="Homo sapiens",
                obs_coords=id_list,
                var_coords=target_gene_ids,
            )
        except:
            target_adata = None
            time.sleep(10)
        if target_adata is None:
            target_adata = cellxgene_census.get_anndata(
                census,
                organism="Homo sapiens",
                obs_coords=id_list,
                var_coords=target_gene_ids,
            )

        census.close()
        joblib.dump(target_adata, save_filename, compress=3)
        print("[saved]",save_filename)
        time.sleep(1)
    
arg_list=[]
for filename in glob.glob("00data/*.obs_id.tsv"):
    cnt=0
    id_list=[]
    for line in open(filename):
        id_list.append(int(line.strip()))
        cnt+=1
    name_,_ = os.path.splitext(os.path.basename(filename))
    name ,_ = os.path.splitext(name_)
    print(name,cnt)
    saved_count=0
    while saved_count<cnt:

        start_l=saved_count
        end_l  =min(saved_count+N,cnt)
        sep_id_list=id_list[start_l:end_l]

        arg_list.append((name,start_l,end_l,sep_id_list))

        saved_count+=N


p = Pool(8)
result=p.map(run, arg_list)


