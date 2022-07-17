with tmp as (
	select 
	tc.id,
--xgb_binary_model.sql内容复制在下面
    case when (GRZHZT is null or GRZHZT < 2) then
        case when (DWSSHY is null or DWSSHY < 15) then
            -0.187160745
        else
            -0.131290004 
        end
    else
        case when (GRZHZT is null or GRZHZT < 5) then
            0.193103448
        else
            0.0526315831 
        end
    end as tree_0_score,

    case when (GRZHZT is null or GRZHZT < 2) then
        case when (DWSSHY is null or DWSSHY < 15) then
            -0.169759557
        else
            -0.118362501 
        end
    else
        case when (GRZHZT is null or GRZHZT < 5) then
            0.17609185
        else
            0.0695680603 
        end
    end as tree_1_score,

    case when (DWSSHY is null or DWSSHY < 15) then
        case when (GRZHZT is null or GRZHZT < 2) then
            -0.156637862
        else
            0.152348146 
        end
    else
        case when (GRYJCE is null or GRYJCE < 747.440002) then
            -0.144210264
        else
            -0.0413662866 
        end
    end as tree_2_score,

    case when (DWSSHY is null or DWSSHY < 15) then
        case when (GRZHZT is null or GRZHZT < 2) then
            -0.146193072
        else
            0.137655646 
        end
    else
        case when (GRYJCE is null or GRYJCE < 747.440002) then
            -0.132047102
        else
            -0.0427833274 
        end
    end as tree_3_score,

    case when (DWJJLX is null or DWJJLX < 185) then
        case when (GRZHZT is null or GRZHZT < 2) then
            -0.136609226
        else
            0.134816915 
        end
    else
        case when (DWJJLX is null or DWJJLX < 195) then
            0.134066537
        else
            -0.116221964 
        end
    end as tree_4_score,

    case when (DWSSHY is null or DWSSHY < 15) then
        case when (GRZHZT is null or GRZHZT < 2) then
            -0.130476803
        else
            0.130891323 
        end
    else
        case when (GRYJCE is null or GRYJCE < 784.942505) then
            -0.111347608
        else
            -0.0214216541 
        end
    end as tree_5_score,

    case when (DWSSHY is null or DWSSHY < 15) then
        case when (GRZHZT is null or GRZHZT < 2) then
            -0.124260537
        else
            0.127549246 
        end
    else
        case when (DWJJLX is null or DWJJLX < 183) then
            -0.0989128947
        else
            0.00076171913 
        end
    end as tree_6_score,

    case when (DWSSHY is null or DWSSHY < 15) then
        case when (GRZHZT is null or GRZHZT < 2) then
            -0.118413165
        else
            0.116782129 
        end
    else
        case when (GRYJCE is null or GRYJCE < 739.307495) then
            -0.103881143
        else
            -0.016469717 
        end
    end as tree_7_score,

    case when (DWJJLX is null or DWJJLX < 177) then
        case when (GRZHZT is null or GRZHZT < 2) then
            -0.111497544
        else
            0.115954496 
        end
    else
        case when (DWJJLX is null or DWJJLX < 195) then
            0.145269901
        else
            -0.0906211212 
        end
    end as tree_8_score,

    case when (DWSSHY is null or DWSSHY < 14) then
        case when (GRZHZT is null or GRZHZT < 2) then
            -0.113653444
        else
            0.111154787 
        end
    else
        case when (DWJJLX is null or DWJJLX < 177) then
            -0.0867692605
        else
            -0.00835803989 
        end
    end as tree_9_score,

    case when (DWSSHY is null or DWSSHY < 14) then
        case when (GRZHZT is null or GRZHZT < 2) then
            -0.109804325
        else
            0.0997169241 
        end
    else
        case when (GRYJCE is null or GRYJCE < 796.142517) then
            -0.0841862187
        else
            -0.00951340701 
        end
    end as tree_10_score,

    case when (DWSSHY is null or DWSSHY < 14) then
        case when (GRZHZT is null or GRZHZT < 2) then
            -0.106502727
        else
            0.0954016969 
        end
    else
        case when (DWJJLX is null or DWJJLX < 177) then
            -0.0773002729
        else
            0.0017032394 
        end
    end as tree_11_score,

    case when (DWSSHY is null or DWSSHY < 15) then
        case when (GRZHZT is null or GRZHZT < 2) then
            -0.0983024165
        else
            0.0977736637 
        end
    else
        case when (GRYJCE is null or GRYJCE < 739.307495) then
            -0.0819410533
        else
            0.00490384735 
        end
    end as tree_12_score,

    case when (DWJJLX is null or DWJJLX < 177) then
        case when (DWJJLX is null or DWJJLX < 115) then
            -0.0677250624
        else
            -0.104051508 
        end
    else
        case when (DWJJLX is null or DWJJLX < 195) then
            0.156660184
        else
            -0.0693324581 
        end
    end as tree_13_score,

    case when (DWSSHY is null or DWSSHY < 14) then
        case when (GRZHZT is null or GRZHZT < 2) then
            -0.0961940736
        else
            0.092902787 
        end
    else
        case when (GRYJCE is null or GRYJCE < 794.790039) then
            -0.0683228895
        else
            0.00111304724 
        end
    end as tree_14_score,

    case when (DWJJLX is null or DWJJLX < 177) then
        case when (DWJJLX is null or DWJJLX < 115) then
            -0.0594243817
        else
            -0.0985846817 
        end
    else
        case when (DWJJLX is null or DWJJLX < 195) then
            0.145852476
        else
            -0.0614285246 
        end
    end as tree_15_score,

    case when (DWSSHY is null or DWSSHY < 14) then
        case when (GRZHZT is null or GRZHZT < 2) then
            -0.0925102383
        else
            0.0896438286 
        end
    else
        case when (GRYJCE is null or GRYJCE < 739.307495) then
            -0.0667830184
        else
            0.00193359354 
        end
    end as tree_16_score,

    case when (DWSSHY is null or DWSSHY < 12) then
        case when (GRZHZT is null or GRZHZT < 2) then
            -0.091098316
        else
            0.0803790987 
        end
    else
        case when (DWJJLX is null or DWJJLX < 177) then
            -0.0561854951
        else
            0.0166140851 
        end
    end as tree_17_score,

    case when (DWSSHY is null or DWSSHY < 14) then
        case when (GRZHZT is null or GRZHZT < 2) then
            -0.0866492614
        else
            0.0918314457 
        end
    else
        case when (GRYJCE is null or GRYJCE < 693.165039) then
            -0.064027369
        else
            -0.00128556869 
        end
    end as tree_18_score,

    case when (DWSSHY is null or DWSSHY < 12) then
        case when (GRZHDNGJYE is null or GRZHDNGJYE < 6326.64014) then
            -0.0887161121
        else
            -0.0191927664 
        end
    else
        case when (GRYJCE is null or GRYJCE < 665.867493) then
            -0.0662619546
        else
            -0.00176904688 
        end
    end as tree_19_score

from train_csv tc
),tmp1 as (
select 
id,
--scores.sql内容复制在下面
tree_0_score+
tree_1_score+
tree_2_score+
tree_3_score+
tree_4_score+
tree_5_score+
tree_6_score+
tree_7_score+
tree_8_score+
tree_9_score+
tree_10_score+
tree_11_score+
tree_12_score+
tree_13_score+
tree_14_score+
tree_15_score+
tree_16_score+
tree_17_score+
tree_18_score+
tree_19_score as score

from tmp
)
select 
t.*,
--用SIGMOD把树分数映射到0-1范围
round(1/(1+exp(-score)),6) as pred
from tmp1 t
where id in (1,2,3,4,5)



