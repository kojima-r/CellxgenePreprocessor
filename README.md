# CellxgenePreprocessor
```
conda install python==3.10
pip install cellxgene_census
pip install joblib
```

## 00build_list.py
- output: `tissue_list.tsv`
- output: `00data/<tissue>.obs_id.tsv`
- output: `00data/<tissue>.var.tsv`

This script lists the target files to be downloaded in the above files.

## 01download.py
- output: `01data/<tissue>-<start>-<end>.jbl`

This script performs the download.
The download is divided into N samples and saved.
This makes it easier to perform parallel processing and allows you to resume from where you left off if the download is interrupted.

## 02conv.py
- output: `02data/<tissue>-<start>-<end>.h5ac`

All downloaded files are converted to standard scanpy files.
This is not done simultaneously with the download to prevent conversion errors from stopping the download.


  
