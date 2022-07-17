
###### theme:模型上线后的稳定性效果评估
###### author:番茄
###### date:20220531


import pandas as pd
import numpy as np


###导入数据
data=pd.read_excel("D:/P3-fanqie/file/data_test_case_article_117.xlsx")


###数据探索
data.shape
data.info()

freq_date=data['date'].value_counts()
freq_date=freq_date.reset_index()
freq_date=freq_date.rename(columns={'index':'date','date':'num'})
freq_date['pct']=freq_date['num']/len(data)


###模型PSI
data_bin=pd.cut(data['score'],10)
data_n=data.loc[:,['date','score']]
data_bin=data_bin.reset_index()
data_n=data_n.reset_index()
data_bin=data_bin.rename(columns={'score':'bin'})
data_bin=data_n.merge(data_bin,on='index',how='inner')
data1=data_bin[(data['date']=='2022/1')]
data2=data_bin[(data['date']=='2022/2')]
data1=data1.loc[:,['score','bin']]
data2=data2.loc[:,['score','bin']]
var_bin1=pd.DataFrame()
var_bin1=data1.groupby(['bin']).count()
var_bin1=var_bin1.reset_index()
var_bin1=var_bin1.rename(columns={'score':'date1_count'})
var_bin2=pd.DataFrame()
var_bin2=data2.groupby(['bin']).count()
var_bin2=var_bin2.reset_index()
var_bin2=var_bin2.rename(columns={'score':'date2_count'})
var_bin3=var_bin1.merge(var_bin2,on='bin',how='inner')
var_bin3.loc['10']=['nan',15701-var_bin3['date1_count'].sum(),
                          14299-var_bin3['date2_count'].sum()] 
var_bin3['date1_pct']=var_bin3['date1_count']/15701
var_bin3['date2_pct']=var_bin3['date2_count']/14299
var_bin3['psi']=(np.log(var_bin3['date1_pct']/var_bin3['date2_pct']))*(var_bin3['date1_pct']-var_bin3['date2_pct'])
var_bin3['psi_sum']=var_bin3['psi'].sum().round(3)


###特征PSI
def var_psi(data,var,cut_num):  
    data_bin=pd.cut(data[var],cut_num)
    data_n=data.loc[:,['date',var]]
    data_bin=data_bin.reset_index()
    data_n=data_n.reset_index()  
    data_bin=data_bin.rename(columns={var:'bin'})  
    data_bin=data_n.merge(data_bin,on='index',how='inner')  
    data1=data_bin[(data['date']=='2022/1')]
    data2=data_bin[(data['date']=='2022/2')]
    data1=data1.loc[:,[var,'bin']]
    data2=data2.loc[:,[var,'bin']]  
    var_bin1=pd.DataFrame()
    var_bin1=data1.groupby(['bin']).count()
    var_bin1=var_bin1.reset_index()
    var_bin1=var_bin1.rename(columns={var:'date1_count'})    
    var_bin2=pd.DataFrame()
    var_bin2=data2.groupby(['bin']).count()
    var_bin2=var_bin2.reset_index()
    var_bin2=var_bin2.rename(columns={var:'date2_count'})
    var_bin3=var_bin1.merge(var_bin2,on='bin',how='inner')
    var_bin3.loc['10']=['nan',15701-var_bin3['date1_count'].sum(),
                              14299-var_bin3['date2_count'].sum()]
    var_bin3['date1_pct']=var_bin3['date1_count']/15701
    var_bin3['date2_pct']=var_bin3['date2_count']/14299
    var_bin3['psi']=(np.log(var_bin3['date1_pct']/var_bin3['date2_pct']))*
                           (var_bin3['date1_pct']-var_bin3['date2_pct'])
    var_bin3['psi_sum']=var_bin3['psi'].sum()
    psi = var_bin3['psi'].sum().round(4)
    print(var,'PSI:',psi)
         
var_psi(data,'x01',5)
var_psi(data,'x02',10)
var_psi(data,'x03',10)
var_psi(data,'x04',10)
var_psi(data,'x05',10)
var_psi(data,'x06',3)  
var_psi(data,'x07',10)
var_psi(data,'x08',10)
var_psi(data,'x09',10)
var_psi(data,'x10',10)  
var_psi(data,'x11',10)
var_psi(data,'x12',10)


###特征CSI-以x01为例
import copy
df=copy.deepcopy(data)

df['x01_bin']=df['x01'].apply(lambda x01:'bin1' if 0<=x01<5.09 
                                   else ('bin2' if 5.09<=x01<5.24
                                   else ('bin3' if 5.24<=x01<5.38
                                   else ('bin4' if 5.38<=x01<5.50
                                   else ('bin5' if 5.50<=x01<5.95
                                   else 'bin6')))))
df_n=df.loc[:,['date','x01_bin']]
data1=df_n[(data['date']=='2022/1')]
data2=df_n[(data['date']=='2022/2')]
var_bin1=pd.DataFrame()
var_bin1=data1.groupby(['x01_bin']).count()
var_bin2=pd.DataFrame()
var_bin2=data2.groupby(['x01_bin']).count()
var_bin1=var_bin1.reset_index()
var_bin2=var_bin2.reset_index()
var_bin1=var_bin1.rename(columns={'date':'date1_count'})
var_bin2=var_bin2.rename(columns={'date':'date2_count'})
var_bin3=var_bin1.merge(var_bin2,on='x01_bin',how='inner')
var_bin3.loc['10']=['nan',15701-var_bin3['date1_count'].sum(),
                          14299-var_bin3['date2_count'].sum()] 
var_bin3['date1_pct']=var_bin3['date1_count']/15701
var_bin3['date2_pct']=var_bin3['date2_count']/14299
var_bin3['differ']=var_bin3['date2_pct']-var_bin3['date1_pct']

var_bin3['score']=var_bin3['x01_bin'].apply(lambda x01_bin:46 if x01_bin=='bin1' 
                                   else (47 if x01_bin=='bin2'
                                   else (49 if x01_bin=='bin3'
                                   else (51 if x01_bin=='bin4'
                                   else (52 if x01_bin=='bin5'
                                   else (55 if x01_bin=='bin6'
                                   else 50))))))
var_bin3['csi']=var_bin3['differ']*var_bin3['score']
var_bin3['csi_sum']=var_bin3['csi'].sum().round(4)







