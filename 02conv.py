import glob
import os
import joblib

from multiprocessing import Pool
import time

os.makedirs("02data/",exist_ok=True)

tissue_list=[]
for filename in glob.glob("00data/*.obs_id.tsv"):
    name_=os.path.basename(filename)
    name_,_=os.path.splitext(name_)
    tissue,_=os.path.splitext(name_)
    print(tissue)
    tissue_list.append(tissue)

arg_list=[]
for tissue in tissue_list:
    for filename in glob.glob("01data/"+tissue+".*.jbl"):
        arg_list.append(filename)

def run(filename):
    print(filename)
    obj=joblib.load(filename)
    name_=os.path.basename(filename)
    name,_=os.path.splitext(name_)
    filename="02data/"+name+".h5ad"
    obj.write_h5ad(filename,compression="gzip")
    #obj.write_h5ad(filename,compression="lzf")


p = Pool(32)
result=p.map(run, arg_list)


