import cellxgene_census
import numpy as np
import pandas as pd
import scanpy as sc
import os
import glob
import joblib

from multiprocessing import Pool
import time


def run(argv):
    census = cellxgene_census.open_soma()
    time.sleep(10)
    time.sleep(10)
    census.close()
p = Pool(8)
result=p.map(run, list(range(10)))


