import psycopg2
import pandas as pd
import time
start_vect=time.time() #런 타임 체크를 위해 삽입

output_name = 'C:/Users/zeno915/Desktop/SQL_TEST1111.xlsx'

user = "zeno915"
password = "Jkh8209$#"
dbname = "sandbox"
host = "dw-sandbox.coupang.net"
port = 5439
conn_str = "dbname='{}' user='{}' host='{}' password='{}' port={}".format(dbname, user, host, password, port)

conn = psycopg2.connect(conn_str)
cursor = conn.cursor()

# q = '''
# select * from information_schema.tables
#
# where table_schema = 'public' order by table_name
# '''


# Daily CSAT 가져오는 쿼리

q = """
/*CS NPS RAW _ wbr*/

SELECT DISTINCT REC.npssurveyid AS 설문번호
    , CASE WHEN CI.mediatype = 'call' THEN 'CALL'
           WHEN CI.mediatype = 'chat' THEN 'LIVECHAT'
           WHEN CI.mediatype = '1on1' THEN 'MAIL'
           WHEN CI.mediatype = 'lazy_chat' THEN 'LAZYCHAT'
           ELSE CI.mediatype END AS 상담경로
    , A.createdat AS 설문발송일시 --?
    , REC.modifiedat AS 설문종료일시
    , CI.inquiryid AS 상담번호
    , A.memberid
    , CI.orderid AS 주문번호
    , CIP.vendoritemid
    , CIP.vendoritemname
    , CI.bigcategoryname AS 문의유형대
    , CI.middlecategoryname AS 문의유형중
    , CI.smallcategoryname AS 문의유형소
    , CASE WHEN CIA.teamname LIKE '%Counie%' OR CIA.teamname LIKE '%Channel%'  OR CIA.teamname LIKE '%CSA%' THEN 'CSA'
           WHEN CIA.teamname LIKE '%KBSJOB%' OR CIA.teamname LIKE '%KTCS%' OR CIA.teamname LIKE '%우리엔유%'
                OR CIA.teamname LIKE '%윌앤비전%' OR CIA.teamname LIKE '%효성ITX%' OR CIA.teamname LIKE '%TCK%' OR CIA.teamname LIKE '%U-BASE%' THEN 'Outsourcing' ELSE 'ETC' END AS 상담조직
    , CASE WHEN CIA.centername = '2센터[종로]' THEN '종로'
           WHEN CIA.centername = '1센터[독산]' THEN '독산' ELSE 'ETC' END AS SITE
    , CASE WHEN CIA.teamname LIKE '%KBSJOB%' THEN 'KBSJOB'
           WHEN CIA.teamname LIKE '%KTCS%' THEN 'KT CS'
           WHEN CIA.teamname LIKE '%우리엔유%' THEN '우리엔유'
           WHEN CIA.teamname LIKE '%윌앤비전%' THEN '윌앤비전'
           WHEN CIA.teamname LIKE '%효성ITX%' THEN '효성ITX'
           WHEN CIA.teamname LIKE '%TCK%' THEN 'TCK'
           WHEN CIA.teamname LIKE '%U-BASE%' THEN 'U-BASE'
           ELSE CIA.teamname END AS 상담센터
    , CIA.agentid AS 처리자ID
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

    , REC.score AS CSAT_5Points
    ,MAX(CASE WHEN DT.detractoritemcode = 'CS007' THEN 1 ELSE 0 END) AS 연결지연
    ,MAX(CASE WHEN DT.detractoritemcode = 'CS008' THEN 1 ELSE 0 END) AS 불친절
    ,MAX(CASE WHEN DT.detractoritemcode = 'CS009' THEN 1 ELSE 0 END) AS 응대불만
    ,MAX(CASE WHEN DT.detractoritemcode = 'CS010' THEN 1 ELSE 0 END) AS 설명부족
    ,MAX(CASE WHEN DT.detractoritemcode = 'CS011' THEN 1 ELSE 0 END) AS 처리지연
    ,MAX(CASE WHEN DT.detractoritemcode = 'CSETC' THEN 1 ELSE 0 END) AS 기타
    , CASE WHEN REC.reason IS NOT NULL THEN REC.reason
           WHEN REC.reason IS NULL THEN REC.detractorreason
           ELSE REC.detractorreason END AS 고객코멘트
    , CASE WHEN CI.biztype = 'RETAIL' THEN 'Retail'
           WHEN CI.biztype = 'THIRDPARTY' AND CIP.vendorid='A00155519' THEN 'Retail'
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
    , CS.comment_rw AS 상담이력
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

FROM ods.nps_processes A
    LEFT JOIN ods.csat_results REC ON A.npssurveyid = REC.npssurveyid
    LEFT JOIN ods.csat_detractor_results DT ON REC.npssurveyid = DT.npssurveyid
    LEFT JOIN ods.customer_inquiries CI ON REC.npssurveyid = CI.npssurveyid
    LEFT JOIN ods.customer_inquiry_agents CIA ON CI.customerinquiryid = CIA.customerinquiryid
    LEFT JOIN ods.csa_inquiries CS ON CI.inquiryid = CS.inquiryId
    LEFT JOIN ods.chat_sessiON CH ON CS.inquiryid = CH.ringinquiryid --EZChat 접수시간
    LEFT JOIN ods.inquiry I ON CH.inquiryid = I.inquiryid --EZChat 접수유형
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
                                , ROW_NUMBER() OVER (PARTITION BY customerinquiryid ORDER BY vendoritemid DESC) AS RANK
                           FROM ods.customer_inquiry_products)
                     WHERE RANK = '1') CIP ON CI.customerinquiryid = CIP.customerinquiryid
    INNER JOIN bimart.dim_date DA   ON DATE(REC.modifiedat) = DA.dates


WHERE 1=1
    AND A.processstatus = 'COMPLETE' -- 설문완료
    AND A.servicetypecode = 'CUSTOMER_INQUIRY' -- CS NPS
    AND DATE(REC.modifiedat) between '2020-04-01' AND '2020-04-30'

GROUP BY 설문번호, 상담경로, 설문발송일시, 설문종료일시, 상담번호, A.memberid, 주문번호, CIP.vendoritemid, CIP.vendoritemname, 문의유형대, 문의유형중, 문의유형소, 상담조직, SITE, 상담센터, 처리자ID, 근속주, 구분, Skilled구분
            , 상담접수일시, 상담완료일시, 처리리드타임, CSAT_5Points, 고객코멘트, 상품유형, CIP.vendorid, CIP.vendorname, CATE1, CATE2, CATE3, CATE4, CIP.delivercompanyname, 상담이력, 주문일
            , CIP.deliverytype, DATE, YYYY_WK기준, wk

ORDER BY REC.npssurveyid ;

"""

cursor.execute(q)

output = cursor.fetchall()
col_names = [desc[0] for desc in cursor.description]

df = pd.DataFrame(output, columns=col_names)

print(df)

df.to_excel(output_name, index=False)

print("training Runtime: %0.2f Minutes"%((time.time() - start_vect)/60)) #런 타임 체크를 위해 삽입