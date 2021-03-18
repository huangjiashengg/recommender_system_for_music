dict1 = {0: 1.0, 6: 1.0}
dict2 = {2714: 3.5356, 4341: 5.868, 324: 4.6577}
dictMerged1 = dict(dict1, **dict2)
print(dictMerged1)