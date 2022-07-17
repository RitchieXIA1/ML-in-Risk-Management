SELECT 
substr(loan_date,1,7) `放款月`
,sum(if(overdue_2m>30 and (repay_date is null or repay_date>add_m2),loan_amount,null))/sum(loan_amount) `+2M坏账率`
,sum(if(overdue_3m>30 and (repay_date is null or repay_date>add_m3),loan_amount,null))/sum(loan_amount) `+3M坏账率`
,sum(if(overdue_4m>30 and (repay_date is null or repay_date>add_m4),loan_amount,null))/sum(loan_amount) `+4M坏账率`
,sum(if(overdue_5m>30 and (repay_date is null or repay_date>add_m5),loan_amount,null))/sum(loan_amount) `+5M坏账率`
,sum(if(overdue_6m>30 and (repay_date is null or repay_date>add_m6),loan_amount,null))/sum(loan_amount) `+6M坏账率`
,sum(if(overdue_7m>30 and (repay_date is null or repay_date>add_m7),loan_amount,null))/sum(loan_amount) `+7M坏账率`
,sum(if(overdue_8m>30 and (repay_date is null or repay_date>add_m8),loan_amount,null))/sum(loan_amount) `+8M坏账率`
,sum(if(overdue_9m>30 and (repay_date is null or repay_date>add_m9),loan_amount,null))/sum(loan_amount) `+9M坏账率`
,sum(if(overdue_10m>30 and (repay_date is null or repay_date>add_m10),loan_amount,null))/sum(loan_amount) `+10M坏账率`
,sum(if(overdue_11m>30 and (repay_date is null or repay_date>add_m11),loan_amount,null))/sum(loan_amount) `+11M坏账率`
,sum(if(overdue_12m>30 and (repay_date is null or repay_date>add_m12),loan_amount,null))/sum(loan_amount) `+12M坏账率`
,sum(if(overdue_13m>30 and (repay_date is null or repay_date>add_m13),loan_amount,null))/sum(loan_amount) `+13M坏账率`
from
(
    SELECT 
    aa.*
    ,max(if(now_date>add_m2 and (repay_date is null or repay_date>add_m2),datediff(dateadd(to_date(add_m2,'yyyy-mm-dd'),3,'dd'),due_date),null))over(partition by order_id) overdue_2m
    ,max(if(now_date>add_m3 and (repay_date is null or repay_date>add_m3),datediff(dateadd(to_date(add_m3,'yyyy-mm-dd'),3,'dd'),due_date),null))over(partition by order_id) overdue_3m
    ,max(if(now_date>add_m4 and (repay_date is null or repay_date>add_m4),datediff(dateadd(to_date(add_m4,'yyyy-mm-dd'),3,'dd'),due_date),null))over(partition by order_id) overdue_4m
    ,max(if(now_date>add_m5 and (repay_date is null or repay_date>add_m5),datediff(dateadd(to_date(add_m5,'yyyy-mm-dd'),3,'dd'),due_date),null))over(partition by order_id) overdue_5m
    ,max(if(now_date>add_m6 and (repay_date is null or repay_date>add_m6),datediff(dateadd(to_date(add_m6,'yyyy-mm-dd'),3,'dd'),due_date),null))over(partition by order_id) overdue_6m
    ,max(if(now_date>add_m7 and (repay_date is null or repay_date>add_m7),datediff(dateadd(to_date(add_m7,'yyyy-mm-dd'),3,'dd'),due_date),null))over(partition by order_id) overdue_7m
    ,max(if(now_date>add_m8 and (repay_date is null or repay_date>add_m8),datediff(dateadd(to_date(add_m8,'yyyy-mm-dd'),3,'dd'),due_date),null))over(partition by order_id) overdue_8m
    ,max(if(now_date>add_m9 and (repay_date is null or repay_date>add_m9),datediff(dateadd(to_date(add_m9,'yyyy-mm-dd'),3,'dd'),due_date),null))over(partition by order_id) overdue_9m
    ,max(if(now_date>add_m10 and (repay_date is null or repay_date>add_m10),datediff(dateadd(to_date(add_m10,'yyyy-mm-dd'),3,'dd'),due_date),null))over(partition by order_id) overdue_10m
    ,max(if(now_date>add_m11 and (repay_date is null or repay_date>add_m11),datediff(dateadd(to_date(add_m11,'yyyy-mm-dd'),3,'dd'),due_date),null))over(partition by order_id) overdue_11m
    ,max(if(now_date>add_m12 and (repay_date is null or repay_date>add_m12),datediff(dateadd(to_date(add_m12,'yyyy-mm-dd'),3,'dd'),due_date),null))over(partition by order_id) overdue_12m
    ,max(if(now_date>add_m13 and (repay_date is null or repay_date>add_m13),datediff(dateadd(to_date(add_m13,'yyyy-mm-dd'),3,'dd'),due_date),null))over(partition by order_id) overdue_13m
    from
    (

        SELECT
        *
        ,substr(datetrunc(getdate(),'month'),1,10) now_date
        ,add_months(substr(loan_date,1,10),2) add_m2
        ,add_months(substr(loan_date,1,10),3) add_m3
        ,add_months(substr(loan_date,1,10),4) add_m4
        ,add_months(substr(loan_date,1,10),5) add_m5
        ,add_months(substr(loan_date,1,10),6) add_m6
        ,add_months(substr(loan_date,1,10),7) add_m7
        ,add_months(substr(loan_date,1,10),8) add_m8
        ,add_months(substr(loan_date,1,10),9) add_m9
        ,add_months(substr(loan_date,1,10),10) add_m10
        ,add_months(substr(loan_date,1,10),11) add_m11
        ,add_months(substr(loan_date,1,10),12) add_m12
        ,add_months(substr(loan_date,1,10),13) add_m13
        FROM vintage_data
    ) aa 
)tt
group by substr(loan_date,1,7)
;