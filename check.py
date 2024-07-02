
import joblib
import numpy as np
obj=joblib.load("01data/nose.00000000-00010000.jbl")
print(obj)
a=obj.X[:3,:3]
print(obj.X[:3,:3].shape)
print(obj.X[:100,:100].todense())

print(obj.var["feature_name"][:10])
print(len(obj.var["feature_name"]))
print(obj.obs["soma_joinid"][:10])
print(len(obj.obs["soma_joinid"]))
print(obj.obs["disease"][:10])
print(obj.obs["tissue"][:10])
print("====")
print(type(obj.X[:10,:10]))
# scipy.sparse._csr.csr_matrix

#print(obj.X[:10,:10])
mat=obj.X[:10,:10].tocoo()
print(mat.data)
print(mat.row)
print(mat.col)

print(mat)

# 10000 × 60664
mat=obj.X[:100,:100]
mat=mat.tocoo()
for r,c,val in zip(mat.row, mat.col, mat.data):
    if val>10:
        a=obj.obs["soma_joinid"]
        b=obj.var["feature_name"]
        print(r,c,"\t",a[r],b[c],val)

#########



