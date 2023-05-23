import pandas as pd
import numpy as np
import time
import os

start_vect=time.time() #런 타임 체크를 위해 삽입

file_locate = "C:/RAW_DATA/Weekly_CSAT/"
file_list = os.listdir(file_locate)
file_list.sort()

#다운 받은 RAW에서 필요한 열만 추출하기
header_list_1 = ['설문번호',"설문종료일시",'상담경로','상담번호','문의유형대','문의유형중','문의유형소','상담조직','상담센터','site','처리자id',
                 '상담완료일시','csat','연결지연','불친절','응대불만','설명부족','처리지연','기타','상품유형','cate1','cate2',
                 'cate3','cate4','구분','skilled구분','yyyy_wk기준','wk']

workbook_combine = []

# 폴더 내에 있는 CSAT RAW 파일을 하나로 합치기
for i in file_list:
    # if i[0:11] == "Daily_CSAT_":
    if i[0:12] == "Weekly_CSAT_":
        print("파일명 ", i, "불러오기 작업을 위해 검사를 시작합니다.")
        workbook = pd.read_excel(file_locate + i, sheet_name="Sheet1", header=2 )
        # RAW 파일이 모든 열을 가지고 있는지 검증하는 작업 (간혹 PowerBI에서 다운로드 시 일부 열이 누락되는 경우 있음)
        if len(workbook.columns) == 62:
            workbook_drop_header = pd.DataFrame(workbook, columns = header_list_1)

            # 데이터 프레임 내 조건별로 새로운 ROW 생성
            workbook_drop_header["CSAT_B"] = workbook_drop_header["csat"].apply(lambda x: 1 if x >= 4 else 0)
            workbook_drop_header["Center_B"] = workbook_drop_header["상담센터"].apply(\
                lambda x: x if x == "KBSJOB" or x == "TCK" or x == "U-BASE" else "CSA")
            workbook_drop_header["IC_Month"] = workbook_drop_header["설문종료일시"].dt.month
            workbook_drop_header["IC_Day"] = workbook_drop_header["설문종료일시"].dt.day
            workbook_drop_header["IC_Weekday"] = workbook_drop_header["설문종료일시"].dt.dayofweek
            workbook_drop_header["IC_Weekend"] = workbook_drop_header["IC_Weekday"].apply(\
                lambda x : 1 if x == 5 or x == 6 else 0)
            workbook_drop_header["IC_Hour"] = workbook_drop_header["설문종료일시"].dt.hour

            # 빈 리스트에 정제된 RAW 파일을 반복 추가
            workbook_combine.append(workbook_drop_header)

            print("파일명 ", i, "불러오기 작업을 완료합니다.")
        else:
            print("파일명 ", i ,"는 다운로드 오류(총 열 수가 62열이 아님)감지되어 건너뜁니다.")

# 리스트 내의 DF들을 하나로 합치는 작업
raw_merger = pd.DataFrame(pd.concat(workbook_combine, sort = False , ignore_index = True))
print("DF를 모아서 하나의 DATAFRAME으로 전환했습니다.")

# 로우를 엑셀파일로 저장
raw_merger.to_excel("C:/RAW_DATA/Daily_CSAT/df_test.xlsx", encoding="EUC-KR")
print("파일 저장을 완료하였습니다.")

# 로우를 CSV파일로 저장
# raw_merger.to_csv("C:/RAW_DATA/Daily_CSAT/df_test.csv", encoding="EUC-KR")



#!----- 상담사의 주(Week) 단위 Multi 스킬 여부를 판단하는 코드
# 원본 소스에서 Multi 스킬을 판단하는데 필요한 열만 추출
print("멀티 상담사 스킬 판단 작업을 시작합니다.")
multi_checker = raw_merger[["처리자id","상담경로","wk","IC_Month"]]
# 새로 생성된 DF를 Pivot Table로 전환
multi_check = pd.pivot_table(multi_checker,index = ["처리자id","wk"] , columns= "상담경로" , values="IC_Month" ,aggfunc= "count" )
print("멀티 상담사 스킬 판단을 위한 피벗 테이블 생성 완료")
# Pivot Table로 전환하게 되면 인덱스가 병합되는 현상이 발생함. 문제 해결을 위해 인덱스 리셋 실행
multi_check_1 = pd.DataFrame(multi_check).reset_index()
# NaN 값을 0으로 변환
multi_check_1 = multi_check_1.fillna(value = 0)
# Multi 판단 결과값을 넣을 열을 생성
multi_check_1["Multiable"] = "MULTI"
# 3개의 열을 비교 분석하여 Multiable 열에 결과값 추가
multi_check_1.loc[(multi_check_1["CALL"]>=0) & (multi_check_1["LAZYCHAT"] ==0)  & (multi_check_1["LIVECHAT"] ==0), "Multiable"] = "CALL"
multi_check_1.loc[(multi_check_1["CALL"]==0) & (multi_check_1["LAZYCHAT"] >=0)  & (multi_check_1["LIVECHAT"] ==0), "Multiable"] = "LAZYCHAT"
multi_check_1.loc[(multi_check_1["CALL"]==0) & (multi_check_1["LAZYCHAT"] ==0)  & (multi_check_1["LIVECHAT"] >=0), "Multiable"] = "LIVECHAT"
print("멀티 상담 여부 체크 완료")
pd.DataFrame(multi_check_1).to_excel('C:/RAW_DATA/Daily_CSAT/multi_test.xlsx', index=False)
print("파일로 저장 완료")
# pd.DataFrame(multi_check).to_excel("C:/RAW_DATA/Daily_CSAT/df_test.xlsx", encoding="EUC-KR")





# print(df_test.columns.tolist())
#
# # df_test.drop(['vendoritemname', 'vendorname','cate1','cate2','cate3','cate4','delivercompanyname',
# #               "inquirycategorylevel1", "inquirycategorylevel2", "inquirycategorylevel3", "fresh_check",
# #               "dawn_check", "normal_check", "ans4_d12", "고객코멘트", "판매자", "판매자구분", "deliverymethod",
# #               "inquirytype2", '상담이력'], axis='columns', inplace=True)
#
# df_test.drop(["vendoritemname", "answer5", "vendorname", "상담이력", "deliverymethod", "channel_ar_group",
#               "channel_ar_group_detail"], axis='columns', inplace=True)
#
# print(df_test.columns.tolist())
# # print(df_test.describe()["csat"])
#
# # df_test.to_csv("C:\\Users\\zeno915\\Desktop\\Daily CSAT\\df_test.csv", encoding="EUC-KR")
#
print("training Runtime: %0.2f Minutes"%((time.time() - start_vect)/60)) #런 타임 체크를 위해 삽입