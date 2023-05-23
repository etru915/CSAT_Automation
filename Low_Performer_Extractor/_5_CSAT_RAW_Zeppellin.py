import pandas as pd
import psycopg2
from pyhive import presto
import numpy as np
import time
import os

def con_server(start_d, end_d):
    start_vect = time.time()  # 런 타임 체크를 위해 삽입
    start_date = int(start_d)
    end_date = int(end_d)

    cursor = presto.connect(host="adhoc-presto-a.coupang.net"
                            , port=443
                            , username='zeno915'
                            , password='jkh8209$#'
                            , protocol='https').cursor()

    que = """
            select *
        from
        (
        select
            c.nps_survey_id
            , c.member_id
            , c.order_id
            , c.survey_create_dt
            , c.inquiry_id
            , c.survey_score
            , case when c.survey_score in (5,4) then 1 else 0 end as csat_s
            , 1 as csat_cnt
            , c.survey_complete_dt
            , c.is_longq
            , c.is_unkindness
            , c.is_consultation
            , c.is_explanation
            , c.is_delayed
            , c.is_other
            , b.detractorreason as comment
            , case when c.media_type_code = 'call' then '1.Call'
                   when c.media_type_code = 'chat' then '2.Live'
                   when c.media_type_code = '1on1' then '4.Mail'
                   when c.media_type_code = 'lazy_chat' then '3.Lazy'
                   else c.media_type_code end as media_type_code
            , substring(cast(c.order_datetime as varchar),1,10) as order_date
            , c.inquiry_category_kor1
            , c.inquiry_category_kor2
            , c.inquiry_category_kor3
            , c.received_datetime
            , c.close_datetime
            , c.inquiry_leadtime
            , case when c.inquiry_leadtime = 0 then 1 else 0 end as sameday_completion
            , case when c.product_category in ('RETAIL', 'WINION') then '1.Retail'
                    when c.product_category = 'THIRDPARTY' and c.vendor_id = 'A00155519' then '1.Retail'
                    when c.product_category = 'THIRDPARTY' THEN '2.3P'
                    when c.product_category = 'ROCKET_JIKGU' THEN '3.Jikgu'
                    when c.product_category = 'TICKET' THEN '4.Travel'
                    when c.product_category = 'OTHERS' THEN '5.Common'
                        else c.product_category end as product_category
            , case when c.team_name like '%CS Operation%' or c.team_name like '%CSA%' or c.team_name like '%Channel%' or c.team_name like '%Counie%' then '1.CSA'
                    when c.team_name like '%KBSJOB%' or c.team_name like '%KTCS%' or c.team_name like '%TCK%' or c.team_name like '%U-BASE%' or c.team_name like '%우리엔유%' or c.team_name like '%윌앤비전%' or c.team_name like '%효성ITX%' then '2.CSAO' else '3.etc' end as team_1
            , case when c.team_name like '%BUCHEON%' then '4.부천'
                    when c.team_name like '%EAST-GATE%' then '3.동대문'
                    when c.center_name = '2센터[종로]' then '1.종로'
                    when c.center_name = '1센터[독산]' then '2.독산' else '5.ETC' end as site
            , case when c.team_name like '%CS Operation%' or c.team_name like '%CSA%' or c.team_name like '%Channel%' or c.team_name like '%Counie%' then '1.CSA'
                    when c.team_name like '%KBSJOB%' then '2.KBSJOB'
                    when c.team_name like '%KTCS%' then '5.ETC'
                    when c.team_name like '%TCK%' then '3.TCK'
                    when c.team_name like '%U-BASE%' then '4.U-BASE'
                    when c.team_name like '%우리엔유%' then '5.ETC'
                    when c.team_name like '%윌앤비전%' then '5.ETC'
                    when c.team_name like '%효성ITX%' then '5.ETC' else '5.ETC' end as team_2
            , c.team_name
            , c.agent_id
            , c.workdays
            , case when c.agent_tenure = 'new' then '1.new'
                    when c.agent_tenure = 'intermediate' then '2.intermediate'
                    when c.agent_tenure = 'skilled' then '3.skilled' else '4.etc' end as agent_tenure
            , case when c.agent_tenure_detail = 'new' then '1.new'
                    when c.agent_tenure_detail = 'intermediate' then '2.intermediate'
                    when c.agent_tenure_detail = 'skilled(03-06)' then '3-1.skilled(03-06)'
                    when c.agent_tenure_detail = 'skilled(06-12)' then '3-2.skilled(06-12)'
                    when c.agent_tenure_detail = 'skilled(12-24)' then '3-3.skilled(12-24)'
                    when c.agent_tenure_detail = 'skilled(24-)' then '3-4.skilled(24-)' else '4.etc' end as agent_tenure_detail
            , c.product_id
            , c.product_name
            , c.vendor_item_id
            , c.vendor_item_name
            , c.management_category_code1
            , c.management_category_code2
            , c.management_category_code3
            , c.management_category_code4
            , c.management_category_code5
            , c.vendor_id
            , c.vendor_name
            , case when c.delivery_method_code = 'SEQUENCIAL' then '1_Sequential delivery(general product)'
                    when c.delivery_method_code = 'VENDOR_DIRECT' then '2_Shipped directly by seller'
                    when c.delivery_method_code = 'MAKE_ORDER' then '3_Custom-made'
                    when c.delivery_method_code = 'INSTRUCTURE' then '4_Installation after delivery'
                    when c.delivery_method_code = 'AGENT_BUY'  then '5_Purchase agency'
                    when c.delivery_method_code = 'COLD_FRESH' then '6_Fresh frozen'
                    when c.delivery_method_code = 'MAKE_ORDER_DIRECT' then '7_Customer-made(shipped directly by seller)'
                    else c.delivery_method_code end as delivery_method
            , c.delivery_name
            , c.source_type
            , c.transfer_type
            , case when c.is_unkindness = 1 or c.is_consultation = 1 or c.is_explanation = 1 then 1 else 0 end as is_agent_reason
            , case when c.is_longq = 1 and c.is_unkindness = 0 and c.is_consultation = 0 and c.is_explanation = 0 and c.is_delayed = 0 then 1 else 0 end as only_is_longq
            , concat(cast(da.iyyyy_1 as varchar),'-',cast(da.mm as varchar),'m') as yyyy_mm_csat
            , concat(cast(da.iyyyy_1 as varchar),'-',cast(da.iyyyy_1_wk as varchar),'wk') as yyyy_wk_csat
            , substring(cast(c.survey_complete_dt as varchar),1,10) as date_csat
            , substring(cast(c.survey_complete_dt as varchar),12,2) as hour_csat
            , c.basis_dy as basis_dy_csat
            , row_number() over (partition by c.inquiry_id order by c.survey_create_dt) as rank
            , case when w.id is not null and date(c.received_datetime) between start_dt and end_dt then '1.Test' else '2.Non-Test' end as warm_gubun_a
            , case when w.id is not null and date(c.received_datetime) between start_dt and end_dt then w.warm_team else 'Non-Test' end as warm_gubun_b
            , case when h.at_home_start is not null and h.at_home_end is not null and (date(c.received_datetime) between h.at_home_start and h.at_home_end) then 'WFH'
            when h.at_home_start is not null and h.at_home_end is null and (date(c.received_datetime) >= h.at_home_start) then 'WFH' else 'WFO' end as wfh_yn
        from sb_fcsystems.dhf_csat_hourly c
            left join ods.csat_results b on c.nps_survey_id = b.npssurveyid
            left join (select warm_team
                            , id
                            , cast(start_dt as date) as start_dt
                            , cast(end_dt as date) as end_dt
        
        from temp.warmtransfer_list) w on c.agent_id = w.id and date(c.received_datetime) between start_dt and end_dt
            left join (select ring_id
                            , cast(at_home_start as date) as at_home_start --재택근무 시작일
                            , case when length(at_home_end) = 0 then date_add('day', -1, current_date) else cast(at_home_end as date) end as at_home_end --재택근무 종료일
                            from temp.at_home_list_dylan) h on c.agent_id = h.ring_id and date(c.received_datetime) between h.at_home_start and h.at_home_end
                            join bimart.dim_date da on date(c.survey_complete_dt) = da.dates
        
        where 1=1
        and c.basis_dy between """+ str(start_date) + " AND " + str(end_date) +" \n"+\
        """
        )
        
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
    con_server(20200831, 20200831)