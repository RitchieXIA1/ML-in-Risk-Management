
###### theme:三方风控数据的测试评估
###### author:番茄风控
###### date:20220405


### step0:算法库定义
import pandas as pd 
import numpy as np


### step1:导入数据
data_test = pd.read_excel("D:XXXX/data_special_course_case_1.xlsx")


### step2:数据探索
#样本量
data_test.shape

#特征类型
data_test.info()

#EDA描述
data_eda = data_test.describe()


### step3:评估维度1-覆盖率
data_miss = data_test[data_test['score_credit'].isnull()
                   & data_test['score_travel'].isnull()
                   & data_test['score_risk_xf'].isnull()
                   & data_test['score_risk_trade'].isnull()
                   & data_test['score_repay'].isnull()
                   & data_test['score_stab_xf'].isnull()]

data_miss.shape      
print((15000-200)/15000)


### step4:评估维度2-缺失率
var_miss = data_test.isnull().sum()
var_miss = var_miss.reset_index()
var_miss = var_miss.rename(columns={'index':'varname',0:'miss_num'})
var_miss['miss_rate']=var_miss['miss_num']/15000
format=lambda x:'%.2f%%' % (x*100)
var_miss['miss_rate']=var_miss['miss_rate'].apply(format)


### step5:评估维度3-有效性
#特征IV-举例score_credit
data_bin=pd.cut(data_test['score_credit'],10)
group_all=data_test['flag'].groupby(data_bin).count()
group_bad=data_test['flag'].groupby(data_bin).sum()
group_good=group_all-group_bad    
var_bin=pd.DataFrame()
var_bin['sum']=group_all
var_bin['bad_count']=group_bad
var_bin['good_count']=group_good
var_bin['bad_rate']=var_bin['bad_count']/var_bin['bad_count'].sum()
var_bin['good_rate']=var_bin['good_count']/var_bin['good_count'].sum()
var_bin['woe']=np.log(var_bin['good_rate']/var_bin['bad_rate'])
var_bin['iv']=var_bin['woe']*(var_bin['good_rate']-var_bin['bad_rate'])
var_bin['iv_sum']=var_bin['iv'].sum().round(3)

#特征IV-批量处理
def var_iv(data,cut_num,var,target):   
    data_cut=pd.cut(data[var],cut_num)
    cut_group_all=data[target].groupby(data_cut).count()
    cut_y=data[target].groupby(data_cut).sum()
    cut_n=cut_group_all-cut_y    
    df=pd.DataFrame()
    df['sum']=cut_group_all
    df['bad_count']=cut_y
    df['good_count']=cut_n
    df['bad_rate']=df['bad_count']/df['bad_count'].sum()
    df['good_rate']=df['good_count']/df['good_count'].sum()    
    df['woe']=np.log(df['bad_rate']/df['good_rate'])
    df['iv']=df['woe']*(df['bad_rate']-df['good_rate'])
    iv=df['iv'].sum().round(3)
    print(var,'IV:',iv)
            
var_iv(data_test,10,'score_credit','flag')
var_iv(data_test,10,'score_travel','flag')
var_iv(data_test,10,'score_risk_xf','flag')
var_iv(data_test,10,'score_risk_trade','flag')
var_iv(data_test,10,'score_repay','flag')
var_iv(data_test,10,'score_stab_xf','flag')    


#特征KS-举例score_credit
var_bin['good_rate_sum']=var_bin['good_rate'].cumsum()
var_bin['bad_rate_sum']=var_bin['bad_rate'].cumsum()
var_bin['ks']=abs(var_bin['good_rate_sum']-var_bin['bad_rate_sum'])
var_bin['ks_max']=var_bin['ks'].max().round(3)

#特征KS-批量处理
def var_ks(data,cut_num,var,target):   
    data_cut=pd.cut(data[var],cut_num)
    cut_group_all=data[target].groupby(data_cut).count()
    cut_y=data[target].groupby(data_cut).sum()
    cut_n=cut_group_all-cut_y    
    df=pd.DataFrame()
    df['sum']=cut_group_all
    df['bad_count']=cut_y
    df['good_count']=cut_n
    df['bad_rate']=df['bad_count']/df['bad_count'].sum()
    df['good_rate']=df['good_count']/df['good_count'].sum()    
    df['good_rate_sum']=df['good_rate'].cumsum()
    df['bad_rate_sum']=df['bad_rate'].cumsum()
    df['ks']=abs(df['good_rate_sum']-df['bad_rate_sum'])
    ks=df['ks'].max().round(3)
    print(var,'KS:',ks)
        
var_ks(data_test,10,'score_credit','flag')
var_ks(data_test,10,'score_travel','flag')
var_ks(data_test,10,'score_risk_xf','flag')
var_ks(data_test,10,'score_risk_trade','flag')
var_ks(data_test,10,'score_repay','flag')
var_ks(data_test,10,'score_stab_xf','flag')    
   
    
### step6:评估维度4-相关性
#pearson系数
var_corr = data_test[['score_credit',
                      'score_travel',
                      'score_risk_xf',
                      'score_risk_trade',
                      'score_repay',
                      'score_stab_xf']].corr(method ='pearson').round(4)


### step7:评估维度5-稳定性
#date分布
date_freq=data_test['date'].groupby(data_test['date']).count()
data_test[(data_test['date']>='2021/02/01')&(data_test['date']<='2021/02/07')].shape
data_test[(data_test['date']>='2021/02/08')&(data_test['date']<='2021/02/15')].shape

#特征psi-举例score_credit
data_bin = pd.cut(data_test['score_credit'],10)
data_test_n = data_test.loc[:,['date','score_credit']]
data_bin = data_bin.reset_index()
data_test_n = data_test_n.reset_index()
data_bin = data_bin.rename(columns={'score_credit':'bin'})
data_test_bin = data_test_n.merge(data_bin,on='index',how='inner')
data_test1 = data_test_bin[(data_test['date']>='2021/02/01')&(data_test['date']<='2021/02/07')]
data_test2 = data_test_bin[(data_test['date']>='2021/02/08')&(data_test['date']<='2021/02/15')]
data_test1 = data_test1.loc[:,['score_credit','bin']]
data_test2 = data_test2.loc[:,['score_credit','bin']]
var_bin1 = pd.DataFrame()
var_bin1 = data_test1.groupby(['bin']).count()
var_bin1 = var_bin1.reset_index()
var_bin1 = var_bin1.rename(columns={'score_credit':'date1_count'})
var_bin2 = pd.DataFrame()
var_bin2 = data_test2.groupby(['bin']).count()
var_bin2 = var_bin2.reset_index()
var_bin2 = var_bin2.rename(columns={'score_credit':'date2_count'})
var_bin3 = var_bin1.merge(var_bin2,on='bin',how='inner')
var_bin3.loc['10'] = ['nan',7218-var_bin3['date1_count'].sum(),
                            7782-var_bin3['date2_count'].sum()] 
var_bin3['date1_pct']=var_bin3['date1_count']/7218
var_bin3['date2_pct']=var_bin3['date2_count']/7782
var_bin3['psi']=(np.log(var_bin3['date1_pct']/var_bin3['date2_pct']))*(var_bin3['date1_pct']-var_bin3['date2_pct'])
var_bin3['psi_sum']=var_bin3['psi'].sum().round(3)

#特征psi-批量处理
def var_psi(data,var,cut_num):  
    data_bin = pd.cut(data[var],cut_num)
    data_test_n = data.loc[:,['date',var]]
    data_bin = data_bin.reset_index()
    data_test_n = data_test_n.reset_index()  
    data_bin = data_bin.rename(columns={var:'bin'})  
    data_test_bin = data_test_n.merge(data_bin,on='index',how='inner')  
    data_test1 = data_test_bin[(data_test['date']>='2021/02/01')&(data_test['date']<='2021/02/07')]
    data_test2 = data_test_bin[(data_test['date']>='2021/02/08')&(data_test['date']<='2021/02/15')]
    data_test1 = data_test1.loc[:,[var,'bin']]
    data_test2 = data_test2.loc[:,[var,'bin']]  
    var_bin1 = pd.DataFrame()
    var_bin1 = data_test1.groupby(['bin']).count()
    var_bin1 = var_bin1.reset_index()
    var_bin1 = var_bin1.rename(columns={var:'date1_count'})    
    var_bin2 = pd.DataFrame()
    var_bin2 = data_test2.groupby(['bin']).count()
    var_bin2 = var_bin2.reset_index()
    var_bin2 = var_bin2.rename(columns={var:'date2_count'})
    var_bin3 = var_bin1.merge(var_bin2,on='bin',how='inner')
    var_bin3.loc['10'] = ['nan',7218-var_bin3['date1_count'].sum(),7782-var_bin3['date2_count'].sum()] 
    var_bin3['date1_pct']=var_bin3['date1_count']/7218
    var_bin3['date2_pct']=var_bin3['date2_count']/7782
    var_bin3['psi']=(np.log(var_bin3['date1_pct']/var_bin3['date2_pct']))*(var_bin3['date1_pct']-var_bin3['date2_pct'])
    var_bin3['psi_sum']=var_bin3['psi'].sum()
    psi = var_bin3['psi'].sum().round(3)
    print(var,'PSI:',psi)
         
var_psi(data_test,'score_credit',10)
var_psi(data_test,'score_travel',10)
var_psi(data_test,'score_risk_xf',10)
var_psi(data_test,'score_risk_trade',10)
var_psi(data_test,'score_repay',10)
var_psi(data_test,'score_stab_xf',10)    


### step8:评估维度6-解释性
#特征分布badrate-举例score_credit
data_bin=pd.cut(data_test['score_credit'],10)
group_all=data_test['flag'].groupby(data_bin).count()
group_bad=data_test['flag'].groupby(data_bin).sum()
group_good=group_all-group_bad    
var_bin=pd.DataFrame()
var_bin['sum']=group_all
var_bin['bad_count']=group_bad
var_bin['good_count']=group_good
var_bin['badrate']=var_bin['bad_count']/(var_bin['good_count']+var_bin['bad_count'])
var_bin['pct']=(var_bin['good_count']+var_bin['bad_count'])/15000
format=lambda x:'%.2f%%' % (x*100)
var_bin['badrate']=var_bin['badrate'].apply(format)
var_bin['pct']=var_bin['pct'].apply(format)    

    
    




