select 
tt.period `期数`,
tt.overdue_rate_0 `0+逾期率`,
tt.overdue_rate_3 `3+逾期率`,
tt.overdue_rate_5 `5+逾期率`,
tt.overdue_rate_7 `7+逾期率`,
tt.overdue_rate_10 `10+逾期率`,
tt.overdue_rate_15 `15+逾期率`,
tt.overdue_rate_30 `30+逾期率`,
tt.overdue_rate_60 `60+逾期率`,
tt.overdue_rate_90 `90+逾期率`
from 
(
    select 
    t.period
    ,count(distinct if(t.due_days>0,t.user_id,null)) as due_user_0 
    ,count(distinct if(t.due_days>0 and t.overdue_days>0,t.user_id,null)) as overdue_user_0
    ,round(count(distinct if(t.due_days>0 and t.overdue_days>0,t.user_id,null))/count(distinct if(t.due_days>0,t.user_id,null)),3) overdue_rate_0

    ,count(distinct if(t.due_days>3,t.user_id,null)) as due_user_3
    ,count(distinct if(t.due_days>3 and t.overdue_days>3,t.user_id,null)) as overdue_user_3
    ,round(count(distinct if(t.due_days>3 and t.overdue_days>3,t.user_id,null))/count(distinct if(t.due_days>3,t.user_id,null)),3) overdue_rate_3

    ,count(distinct if(t.due_days>5,t.user_id,null)) as due_user_5
    ,count(distinct if(t.due_days>5 and t.overdue_days>5,t.user_id,null)) as overdue_user_5
    ,round(count(distinct if(t.due_days>5 and t.overdue_days>5,t.user_id,null))/count(distinct if(t.due_days>5,t.user_id,null)),3) overdue_rate_5

    ,count(distinct if(t.due_days>7,t.user_id,null)) as due_user_7
    ,count(distinct if(t.due_days>7 and t.overdue_days>7,t.user_id,null)) as overdue_user_7
    ,round(count(distinct if(t.due_days>7 and t.overdue_days>7,t.user_id,null))/count(distinct if(t.due_days>7,t.user_id,null)),3) overdue_rate_7

    ,count(distinct if(t.due_days>10,t.user_id,null)) as due_user_10
    ,count(distinct if(t.due_days>10 and t.overdue_days>10,t.user_id,null)) as overdue_user_10
    ,round(count(distinct if(t.due_days>10 and t.overdue_days>10,t.user_id,null))/count(distinct if(t.due_days>10,t.user_id,null)),3) overdue_rate_10

    ,count(distinct if(t.due_days>15,t.user_id,null)) as due_user_15
    ,count(distinct if(t.due_days>15 and t.overdue_days>15,t.user_id,null)) as overdue_user_15
    ,round(count(distinct if(t.due_days>15 and t.overdue_days>15,t.user_id,null))/count(distinct if(t.due_days>15,t.user_id,null)),3) overdue_rate_15

    ,count(distinct if(t.due_days>30,t.user_id,null)) as due_user_30
    ,count(distinct if(t.due_days>30 and t.overdue_days>30,t.user_id,null)) as overdue_user_30
    ,round(count(distinct if(t.due_days>30 and t.overdue_days>30,t.user_id,null))/count(distinct if(t.due_days>30,t.user_id,null)),3) overdue_rate_30

    ,count(distinct if(t.due_days>60,t.user_id,null)) as due_user_60
    ,count(distinct if(t.due_days>60 and t.overdue_days>60,t.user_id,null)) as overdue_user_60
    ,round(count(distinct if(t.due_days>60 and t.overdue_days>60,t.user_id,null))/count(distinct if(t.due_days>60,t.user_id,null)),3) overdue_rate_60

    ,count(distinct if(t.due_days>90,t.user_id,null)) as due_user_90
    ,count(distinct if(t.due_days>90 and t.overdue_days>90,t.user_id,null)) as overdue_user_90
    ,round(count(distinct if(t.due_days>90 and t.overdue_days>90,t.user_id,null))/count(distinct if(t.due_days>90,t.user_id,null)),3) overdue_rate_90
    from 
    (
       select 
       *
       ,datediff(getdate(),to_date(due_date,'yyyy-mm-dd'),'dd') as due_days 
       ,datediff(if((repay_time is null or substr(repay_time,1,10)>=substr(getdate(),1,10)),getdate(),repay_time),to_date(due_date,'yyyy-mm-dd'),'dd') as overdue_days
       from overdue_rate_data
    ) t
    group by t.period
) tt;