import cellxgene_census
import numpy as np
import pandas as pd
import scanpy as sc
import os
census = cellxgene_census.open_soma()

summary_table = census["census_info"]["summary_cell_counts"].read().concat().to_pandas()
summary_table=summary_table.query("organism == 'Homo sapiens' & category == 'tissue_general'")

tissue_list=summary_table["label"].unique().tolist()

with open("tissue_list.tsv","w") as fp:
    for el in tissue_list:
        fp.write(el)
        fp.write("\n")

os.makedirs("00data/",exist_ok=True)

for target_tissue in tissue_list:
    print("...",target_tissue)
    tissue_obs = (
        census["census_data"]["homo_sapiens"]
        .obs.read(value_filter="tissue_general == '"+target_tissue+"' and is_primary_data == True")
        .concat()
        .to_pandas()
    )
    census_datasets = (
        census["census_info"]["datasets"]
        .read(column_names=["collection_name", "dataset_title", "dataset_id", "soma_joinid"])
        .concat()
        .to_pandas()
    )
    dataset_cell_counts = pd.DataFrame(tissue_obs[["dataset_id"]].value_counts())
    dataset_cell_counts = dataset_cell_counts.rename(columns={0: "cell_counts"})
    dataset_cell_counts = dataset_cell_counts.merge(census_datasets, on="dataset_id")

    #presence_matrix = cellxgene_census.get_presence_matrix(census, "Homo sapiens", "RNA")
    #presence_matrix = presence_matrix[dataset_cell_counts.soma_joinid, :]

    tissue_var = census["census_data"]["homo_sapiens"].ms["RNA"].var.read().concat().to_pandas()
    filename="00data/"+target_tissue+".var.tsv"
    tissue_var.to_csv(filename, sep='\t')
    print("[save]",filename)
    
    filename="00data/"+target_tissue+".obs_id.tsv"
    with open(filename,"w") as fp:
        for el in tissue_obs["soma_joinid"]:
            fp.write(str(el))
            fp.write("\n")
    print("[save]",filename)

