import pandas as pd
import psycopg2
from pyhive import presto
import numpy as np
import time
import os

def con_server(start_d, end_d):
    start_vect = time.time()  # 런 타임 체크를 위해 삽입
    start_date = start_d
    end_date = end_d

    cursor = presto.connect(host="adhoc-presto-a.coupang.net"
                            , port=443
                            , username='zeno915'
                            , password='jjangkyo21$$'
                            , protocol='https').cursor()
    que = """
        select *
        from
            (
            select
                case when c.team_name like '%CS Operation%' or c.team_name like '%CSA%' or c.team_name like '%Channel%' or c.team_name like '%Counie%' then '1.CSA'
                     when c.team_name like '%KBSJOB%' or c.team_name like '%KTCS%' or c.team_name like '%TCK%' or c.team_name like '%U-BASE%' or c.team_name like '%우리엔유%' or c.team_name like '%윌앤비전%' or c.team_name like '%효성ITX%' then '2.CSAO' else '3.etc' end as team_1
                , c.team_name
                , case when c.media_type_code = 'call' then '1.Call'
                       when c.media_type_code = 'chat' then '2.Live'
                       when c.media_type_code = '1on1' then '4.Mail'
                       when c.media_type_code = 'lazy_chat' then '3.Lazy'
                       else c.media_type_code end as media_type_code
                , case when c.team_name like '%BUCHEON%' then '4.부천'
                       when c.team_name like '%EAST-GATE%' then '3.동대문'
                       when c.center_name = '2센터[종로]' then '1.종로' 
                       when c.center_name = '1센터[독산]' then '2.독산' else '5.ETC' end as site
                , c.nps_survey_id
                , c.survey_create_dt
                , c.survey_complete_dt
                , c.inquiry_id
                , c.member_id
                , c.order_id
                , c.vendor_item_id
                , c.inquiry_category_kor1
                , c.inquiry_category_kor2
                , c.inquiry_category_kor3
                , case when c.team_name like '%CS Operation%' or c.team_name like '%CSA%' or c.team_name like '%Channel%' or c.team_name like '%Counie%' then '1.CSA'
                       when c.team_name like '%KBSJOB%' then '2.KBSJOB'
                       when c.team_name like '%KTCS%' then '5.ETC'
                       when c.team_name like '%TCK%' then '3.TCK'
                       when c.team_name like '%U-BASE%' then '4.U-BASE'
                       when c.team_name like '%우리엔유%' then '5.ETC'
                       when c.team_name like '%윌앤비전%' then '5.ETC'
                       when c.team_name like '%효성ITX%' then '5.ETC' else '5.ETC' end as team_2
                , c.agent_id
                , c.agent_tenure
                , c.agent_tenure_detail
                , c.received_datetime
                , c.close_datetime
                , c.inquiry_leadtime	
                , c.survey_score
                , c.is_longq
                , c.is_unkindness
                , c.is_consultation
                , c.is_explanation
                , c.is_delayed
                , c.is_other
                , b.detractorreason as comment
                , case when c.product_category in ('RETAIL', 'WINION') then '1.Retail'
                       when c.product_category = 'THIRDPARTY' and c.vendor_id = 'A00155519' then '1.Retail' 	
                       when c.product_category = 'THIRDPARTY' THEN '2.3P'
                       when c.product_category = 'ROCKET_JIKGU' THEN '3.Jikgu'
                       when c.product_category = 'TICKET' THEN '4.Travel'
                       when c.product_category = 'OTHERS' THEN '5.Common'
                       else c.product_category end as product_category
                , c.delivery_name
                , c.source_type
                , concat(cast(da.iyyyy_1 as varchar),'-',cast(da.mm as varchar),'m') as yyyy_mm
                , concat(cast(da.iyyyy_1 as varchar),'-',cast(da.iyyyy_1_wk as varchar),'wk') as yyyy_wk
                , substring(cast(c.survey_complete_dt as varchar),1,10) as date
                , row_number() over(partition by c.inquiry_id order by c.survey_create_dt) as rank
            from sb_fcsystems.dhf_csat_hourly c
                left join ods.csat_results b on c.nps_survey_id = b.npssurveyid
                join bimart.dim_date da on date(c.survey_complete_dt) = da.dates
            where 1=1
                and cast(c.basis_dy as varchar) between """+ str(start_date) + " AND " + str(end_date) +" \n"+\
        """
            )
        where rank = 1 
        
        """



 # execute query phrase
    execute = cursor.execute(que)
    print("쿼리 실행 시작")

    # fetch and assign query ressult
    fetchall = cursor.fetchall()

    # session close
    close = cursor.close()
    print("쿼리 실행 완료")

    # set column names from query result
    col_names = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(fetchall, columns=col_names)
    print("DF 변환")
    df.to_excel("C:/Users/zeno915/Desktop/pycharm/CSAT_Raw.xlsx", encoding="EUC-KR", engine ='xlsxwriter')

    print("training Runtime: %0.2f Minutes" % ((time.time() - start_vect) / 60))  # 런 타임 체크를 위해 삽입

if __name__ == "__main__":
    # 20200401, 2020-04-30 형식으로 입력"
    con_server("'20201217'", "'20201231'")
