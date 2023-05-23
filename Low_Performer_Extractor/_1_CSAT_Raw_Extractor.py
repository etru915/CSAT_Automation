import pandas as pd
import psycopg2
import numpy as np
import time
import os


# "'2020-04-01', '2020-04-30' 형식으로 입력"

def con_server(start_d, end_d):
    start_vect = time.time()  # 런 타임 체크를 위해 삽입
    start_date = str("'" + start_d + "'")
    end_date = str("'" + end_d + "'")
    user = "zeno915"
    password = "Jjangkyo21$$"
    dbname = "sandbox"
    host = "dw-sandbox.coupang.net"
    port = 5439
    conn_str = "dbname='{}' user='{}' host='{}' password='{}' port={}".format(dbname, user, host, password, port)

    conn = psycopg2.connect(conn_str)
    cursor = conn.cursor()

    q = """
    /*CS CSAT 공유_200526*/

    SELECT DISTINCT REC.npssurveyid AS 설문번호
        , CASE WHEN CI.mediatype = 'call' THEN 'CALL'
               WHEN CI.mediatype = 'chat' THEN 'LIVECHAT'
            WHEN CI.mediatype = '1on1' THEN 'MAIL'
            WHEN CI.mediatype = 'lazy_chat' THEN 'LAZYCHAT'
           ELSE CI.mediatype END AS 상담경로
        , A.createdat AS 설문발송일시
        , REC.modifiedat AS 설문종료일시
        , CI.inquiryid AS 상담번호
        , A.memberid 
        , CI.orderid AS 주문번호
        , CIP.vendoritemid
        , CIP.vendoritemname
        , CI.bigcategoryname AS 문의유형대
        , CI.middlecategoryname AS 문의유형중
        , CI.smallcategoryname AS 문의유형소
            , CASE WHEN CIA.teamname LIKE '%Counie%' OR CIA.teamname LIKE '%Channel%' OR CIA.teamname LIKE '%CSA%' THEN 'CSA'
                WHEN CIA.teamname LIKE '%Seller%' THEN 'ETC'
                WHEN CIA.teamname LIKE '%KBSJOB%' OR CIA.teamname LIKE '%KTCS%' OR CIA.teamname LIKE '%우리엔유%' OR CIA.teamname LIKE '%윌앤비전%' OR CIA.teamname LIKE '%효성ITX%' OR CIA.teamname LIKE '%TCK%' OR CIA.teamname LIKE '%U-BASE%' THEN 'CSAO'
                ELSE 'ETC' END AS 상담조직
            , CASE WHEN CIA.teamname LIKE '%BUCHEON%' THEN '부천'
                WHEN CIA.teamname LIKE '%EAST-GATE%' THEN '신설동'
                WHEN CIA.centername = '2센터[종로]' THEN '종로'
                WHEN CIA.centername = '1센터[독산]' THEN '독산'
                ELSE 'ETC' END AS SITE
            , CASE WHEN CIA.teamname LIKE '%KBSJOB%' THEN 'KBSJOB'
                WHEN CIA.teamname LIKE '%KTCS%' THEN 'KT CS'
                WHEN CIA.teamname LIKE '%우리엔유%' THEN '우리엔유'
                WHEN CIA.teamname LIKE '%윌앤비전%' THEN '윌앤비전'
                WHEN CIA.teamname LIKE '%효성ITX%' THEN '효성ITX'
                WHEN CIA.teamname LIKE '%TCK%' THEN 'TCK'
                WHEN CIA.teamname LIKE '%U-BASE%' THEN 'U-BASE'
                ELSE CIA.teamname END AS 상담센터
        , CIA.agentid AS 처리자ID
            ,U.joindate
        , (CIA.workdays/7) AS 근속주
        , CASE WHEN (CIA.workdays/7) >= 0 AND (CIA.workdays/7) <= 4 THEN 'New'
            WHEN (CIA.workdays/7) > 4 AND (CIA.workdays/7) <= 8 THEN 'Intermediate'
            WHEN (CIA.workdays/7) > 8 THEN 'skilled' ELSE 'Etc' END AS 구분
           
    , CASE WHEN (CIA.workdays/7) >= 0 AND (CIA.workdays/7) <= 4 THEN 'New' 
           WHEN (CIA.workdays/7) > 4 AND (CIA.workdays/7) <= 8 THEN 'Intermediate'
           WHEN (CIA.workdays/7) > 8 AND (CIA.workdays/7) <= 24 THEN 'Skilled(03-06)'
           WHEN (CIA.workdays/7) > 24 AND (CIA.workdays/7) <= 48 THEN 'Skilled(06-12)'
           WHEN (CIA.workdays/7) > 48 AND (CIA.workdays/7) <= 96 THEN 'Skilled(12-24)'
           WHEN (CIA.workdays/7) > 96 THEN 'Skilled(24-)' ELSE 'Etc' END AS Skilled구분               

    , CI.inquirystartat AS 상담접수일시
    , CI.inquiryendat AS 상담완료일시
    , DATEDIFF(DAY, CI.inquirystartat, CI.inquiryendat) AS 처리리드타임

    , REC.score AS CSAT
    , MAX(CASE WHEN DT.detractoritemcode IN ('CS007', 'ZCS007') THEN 1 ELSE 0 END) AS 연결지연 
    , MAX(CASE WHEN DT.detractoritemcode IN ('CS008', 'ZCS008') THEN 1 ELSE 0 END) AS 불친절 
    , MAX(CASE WHEN DT.detractoritemcode IN ('CS009', 'ZCS009') THEN 1 ELSE 0 END) AS 응대불만 
    , MAX(CASE WHEN DT.detractoritemcode IN ('CS010', 'ZCS010') THEN 1 ELSE 0 END) AS 설명부족 
    , MAX(CASE WHEN DT.detractoritemcode IN ('CS011', 'ZCS011') THEN 1 ELSE 0 END) AS 처리지연 
    , MAX(CASE WHEN DT.detractoritemcode IN ('CSETC', 'ZCSETC') THEN 1 ELSE 0 END) AS 기타
    , CASE WHEN REC.reason IS NOT NULL THEN REC.reason
           WHEN REC.reason IS NULL THEN REC.detractorreason 
           ELSE REC.detractorreason END AS 고객코멘트
           , CASE WHEN CI.biztype IN ('RETAIL', 'WINION') THEN 'Retail'
                WHEN CI.biztype = 'THIRDPARTY' AND CIP.vendorid = 'A00155519' THEN 'Retail'
                WHEN CI.biztype = 'THIRDPARTY' THEN '3P'
                WHEN CI.biztype = 'ROCKET_JIKGU' THEN 'Rocket_Jikgu'
                WHEN CI.biztype = 'TICKET' THEN 'Ticket'
                WHEN CI.biztype = 'OTHERS' THEN 'Others'
                ELSE CI.biztype END AS 상품유형
                
    , CIP.vendorid
    , CIP.vendorname
    , CIP.productcategory1 AS CATE1
    , CIP.productcategory2 AS CATE2
    , CIP.productcategory3 AS CATE3
    , CIP.productcategory4 AS CATE4
    , CIP.delivercompanyname
    , SUBSTRING(CI.orderedat,1,10) AS 주문일
    , CASE WHEN CIP.deliverytype = 'SEQUENCIAL' THEN '1_Sequential delivery (general product)'
           WHEN CIP.deliverytype = 'VENDOR_DIRECT' THEN '2_Shipped directly by seller'
           WHEN CIP.deliverytype = 'MAKE_ORDER' THEN '3_Custom-made'
           WHEN CIP.deliverytype = 'INSTRUCTURE' THEN '4_Installation after delivery'
           WHEN CIP.deliverytype = 'AGENT_BUY'  THEN '5_Purchase agency'
           WHEN CIP.deliverytype = 'COLD_FRESH' THEN '6_Fresh frozen'
           WHEN CIP.deliverytype = 'MAKE_ORDER_DIRECT' THEN '7_Customer-made (shipped directly by seller)'
           ELSE CIP.deliverytype END AS deliverymethod
    , DATE(REC.modifiedat) AS DATE
    , iyyyy_1 AS YYYY_WK기준
    , DA.iyyyy_1_wk AS WK
        ,CASE WHEN A.servicetypecode = 'CUSTOMER_INQUIRY' THEN 'Ring'
            WHEN A.servicetypecode = 'ZD_CUSTOMER_INQUIRY' THEN 'Zendesk' END AS servicetypecode
            
    FROM ( SELECT DISTINCT npssurveyid, memberid, createdat, servicetypecode
        FROM ods.nps_processes
        WHERE 1=1
            AND processstatus = 'COMPLETE' -- 설문완료
            AND servicetypecode IN ('CUSTOMER_INQUIRY', 'ZD_CUSTOMER_INQUIRY') -- CS NPS
        ) A
        
        INNER JOIN ( SELECT DISTINCT npssurveyid, modifiedat, score, reason, detractorreason
                    FROM ods.csat_results CR
                    WHERE 1=1
                    AND DATE(CR.modifiedat) BETWEEN""" + start_date + " AND " + end_date +"\n"+\
    """
    ) REC ON A.npssurveyid = REC.npssurveyid
    
    LEFT JOIN ods.csat_detractor_results DT ON REC.npssurveyid = DT.npssurveyid
    LEFT JOIN ods.customer_inquiries CI ON REC.npssurveyid = CI.npssurveyid
    LEFT JOIN ods.customer_inquiry_agents CIA ON CI.customerinquiryid = CIA.customerinquiryid
    LEFT JOIN ods.cssec_cs_user U ON CIA.agentid = U.userid
    LEFT JOIN (SELECT customerinquiryid 
                            , productname
                            , vendoritemid
                            , vendoritemname
                            , productcategory1
                            , productcategory2
                            , productcategory3
                            , productcategory4
                            , productcategory5
                            , vendorid
                            , vendorname
                            , deliverytype
                            , delivercompanyname 
                     FROM (SELECT customerinquiryid
                                , productname
                                , vendoritemid
                                , vendoritemname
                                , productcategory1
                                , productcategory2
                                , productcategory3
                                , productcategory4
                                , productcategory5
                                , vendorid
                                , vendorname
                                , deliverytype
                                , delivercompanyname  
                                , ROW_NUMBER() OVER (PARTITION BY customerinquiryid ORDER BY vendoritemid) AS RANK
                           FROM ods.customer_inquiry_products)
                     WHERE RANK = '1') CIP ON CI.customerinquiryid = CIP.customerinquiryid
                     
    INNER JOIN bimart.dim_date DA   ON DATE(REC.modifiedat) = DA.dates
    WHERE 1=1
        AND CI.mediatype <> 'qa'
    
    GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45
    
    ORDER BY REC.modifiedat ;
        """

    cursor.execute(q)
    print("쿼리 실행 시작")

    output = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    print("쿼리 실행 완료")

    df = pd.DataFrame(output, columns=col_names)
    print("DF 변환")
    df.to_excel("C:/Users/zeno915/Desktop/pycharm/CSAT_Raw.xlsx", encoding= "EUC-KR")

    print("training Runtime: %0.2f Minutes" % ((time.time() - start_vect) / 60))  # 런 타임 체크를 위해 삽입
    return df



if __name__ == "__main__":
    # '2020-04-01', '2020-04-30' 형식으로 입력"
    con_server('2020-08-18', '2020-08-19')

