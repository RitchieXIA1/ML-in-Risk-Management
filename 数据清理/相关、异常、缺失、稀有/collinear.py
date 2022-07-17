# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 13:01:00 2020

"""
import gc
import pandas as pd
import numpy as np


def nan_search(data=None):
    nans_df = data.isna()
    nans_groups={}
    for col in data.columns:
        cur_group = nans_df[col].sum()
        try:
            nans_groups[cur_group].append(col)
        except:
            nans_groups[cur_group]=[col]
    del nans_df; 
    gc.collect()
    length=data.shape[0]
    groups=[]
    ratio=[]
    for k,v in nans_groups.items():
        
        print('####### NAN count =',k)
        print('####### NAN ratio =',k/length)
        ratio.append(k/length)
        print(v)
        groups.append(v)
        print('\n')
    return groups,ratio
        
def reduce_group(data,cols):
    drops = []
    for g in cols:
        mx = 0; vx = g[0]
        for gg in g:
            n = data[gg].nunique()
            if n>mx:
                mx = n
                vx = gg
        g.remove(vx)
        drops.append(g)
    print('drop these',drops)
    return drops




def identify_collinear(corr_matrix,correlation_threshold,X):
    
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k = 1).astype(np.bool))
    
    # Select the features with correlations above the threshold
    # Need to use the absolute value
    to_drop = [column for column in upper.columns if any(upper[column].abs() > correlation_threshold)]
    
    # Dataframe to hold correlated pairs
    record_collinear = pd.DataFrame(columns = ['corr_feature1', 'corr_feature2', 'corr_value'])
    
    # Iterate through the columns to drop to record pairs of correlated features
    for column in to_drop:
    
        # Find the correlated features
        corr_features = list(upper.index[upper[column].abs() > correlation_threshold])
    
        # Find the correlated values
        corr_values = list(upper[column][upper[column].abs() > correlation_threshold])
        drop_features = [column for _ in range(len(corr_features))]    
    
        # Record the information (need a temp df for now)
        temp_df = pd.DataFrame.from_dict({'corr_feature1': drop_features,
                                         'corr_feature2': corr_features,
                                         'corr_value': corr_values})
    
        # Add to dataframe
        record_collinear = record_collinear.append(temp_df, ignore_index = True)
    drops=[]## 下面是删除规则
    if record_collinear.shape[0]==0:
        return 'nothing!','nothing!'
    for i,j in zip(record_collinear.corr_feature1.values.tolist(),record_collinear.corr_feature2.values.tolist()):
        if X[i].nunique()>X[j].nunique():
            drops.append(j)
        else:
            drops.append(i)
    drops=list(set(drops))
    return record_collinear,drops






