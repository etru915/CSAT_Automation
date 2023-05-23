import pandas as pd
import numpy as np
import time
import os

start_vect=time.time() #런 타임 체크를 위해 삽입

file_locate = "C:/RAW_DATA/CSAT_Refine/CSAT_raw_refine_0203_0418.xlsx"
# file_locate = "C:/RAW_DATA/Daily_CSAT/df_test.xlsx" # 테스트용 DB

save_locate = "C:/RAW_DATA/Outliner_Extract/"

workbook = pd.read_excel(file_locate, sheet_name="Sheet1", header=0 )

workbook = workbook.loc[workbook["IC_Month"] == 4]
workbook.to_excel(save_locate + '4월 전체 RAW.xlsx', index=True)


# !------ 전체/ 채널별 CSAT %, CSAT #, SAMPLE 을 추출

# 전체 RAW CSAT %, CSAT #, SAMPLE
print("\n------------전체 지표---------------\n")
total_mean = workbook["CSAT_B"].mean().round(4)
print("전체 CSAT % -- >\n ", total_mean)
total_count = workbook["CSAT_B"].count()
print("전체 Sample -- >\n ", total_count)
total_sum = workbook["CSAT_B"].sum()
print("전체 CSAT # -- >\n ", total_sum)

# !------ 전체 RAW를 채널별로 그룹화한 CSAT %, CSAT #, SAMPLE
print("\n------------채널별 지표---------------\n")
channel_mean = workbook.groupby(["상담경로"], as_index= True).mean()
channel_mean_dict = dict(channel_mean["CSAT_B"].round(4))
print("채널별 CSAT % -- >\n ", channel_mean_dict)
channel_count = workbook.groupby(["상담경로"], as_index= True).count()
channel_count_dict = dict(channel_count["CSAT_B"].round(4))
print("채널별 Sample -- >\n ", channel_count_dict)
channel_sum = workbook.groupby(["상담경로"], as_index= True).sum()
channel_sum_dict = dict(channel_sum["CSAT_B"].round(4))
print("채널별 CSAT # -- >\n ", channel_sum_dict)


print("\n------------상담사별 지표---------------\n")

# !------ 전체 RAW를 상담사별로 그룹화한 CSAT %, CSAT #, SAMPLE
# 상담사별 / 상담경로 별 Sample 피벗테이블 생성
channel_check = workbook[["처리자id","상담경로","wk","IC_Month","CSAT_B"]]
id_channel_csat = pd.pivot_table(workbook, index = ["처리자id"], columns="상담경로", values="CSAT_B", aggfunc="count")
id_channel_csat.rename(columns={'CALL': 'CALL_count', 'LAZYCHAT': 'LAZYCHAT_count', 'LIVECHAT': "LIVECHAT_count"}, inplace=True)
id_channel_csat_count_dict  = dict(id_channel_csat.count())
print("상담사별 / 상담경로 별 전체 인원 수 -- >\n ", id_channel_csat_count_dict)


# 상담사별 / 상담경로 별 CSAT # 피벗테이블 생성
channel_check = workbook[["처리자id","상담경로","wk","IC_Month","CSAT_B"]]
id_channel_sample = pd.pivot_table(workbook, index = ["처리자id"], columns="상담경로", values="CSAT_B", aggfunc="sum")
id_channel_sample.rename(columns={'CALL': 'CALL_sum', 'LAZYCHAT': 'LAZYCHAT_sum', 'LIVECHAT': "LIVECHAT_sum"}, inplace=True)
id_channel_sample_sum_dict  = dict(id_channel_sample.sum())
print("상담사별 / 상담경로 별 CSAT # -- >\n ", id_channel_sample_sum_dict)

# 상담사별 / 상담경로 별 CSAT % 피벗테이블 생성
channel_check = workbook[["처리자id","상담경로","wk","IC_Month","CSAT_B"]]
id_channel_avg = pd.pivot_table(workbook, index = ["처리자id"], columns="상담경로", values="CSAT_B", aggfunc="mean")
id_channel_avg.rename(columns={'CALL': 'CALL_mean', 'LAZYCHAT': 'LAZYCHAT_mean', 'LIVECHAT': "LIVECHAT_mean"}, inplace=True)
id_channel_avg = id_channel_avg.round(4)
id_channel_csat_avg_dict  = dict(id_channel_avg.mean().round(4))
print("상담사별 / 상담경로 별 CSAT %(평균의 평균 오류값) -- >\n ", id_channel_csat_avg_dict)

# !-- SUM DF , COUNT DF, MEAN DF 합쳐서 하나의 파일 만들기 (방법 1)
channel_check = pd.concat([id_channel_csat, id_channel_sample, id_channel_avg], axis=1)

# !-- SUM DF , COUNT DF, MEAN DF 합쳐서 하나의 파일 만들기 (방법 2)
# channel_check = pd.merge(channel_check_sum , channel_check_count, how = "outer", left_index= True, right_index= True )
# channel_check["CALL_avg"] = channel_check['CALL_sum'] / channel_check['CALL_count']
# channel_check["CALL_avg"] = channel_check["CALL_avg"].round(2)
# channel_check["LAZYCHAT_avg"] = channel_check['LAZYCHAT_sum'] / channel_check['LAZYCHAT_count']
# channel_check["LAZYCHAT_avg"] = channel_check["LAZYCHAT_avg"].round(2)
# channel_check["LIVECHAT_avg"] = channel_check['LIVECHAT_sum'] / channel_check['LIVECHAT_count']
# channel_check["LIVECHAT_avg"] = channel_check["LIVECHAT_avg"].round(2)
# channel_check = channel_check[["CALL_sum","CALL_count","CALL_avg","LAZYCHAT_sum","LAZYCHAT_count","LAZYCHAT_avg",
#                                "LIVECHAT_sum","LIVECHAT_count","LIVECHAT_avg"]]

# !-- Low Perfomer 선정을 위한 기준 지표 설정하기
print("\n------------채널별 Outliner 기준 지표---------------\n")


call_csat_Indicator = channel_mean_dict["CALL"]
print("call_csat_Indicator-->" , call_csat_Indicator)
call_sample_Indicator = round((id_channel_sample_sum_dict["CALL_sum"] / id_channel_csat_count_dict["CALL_count"]/2),0)
print("call_sample_Indicator-->" , call_sample_Indicator)

lazy_csat_Indicator = channel_mean_dict["LAZYCHAT"]
print("lazy_csat_Indicator-->" , lazy_csat_Indicator)
lazy_sample_Indicator = round((id_channel_sample_sum_dict["LAZYCHAT_sum"] / id_channel_csat_count_dict["LAZYCHAT_count"]/2),0)
print("lazy_sample_Indicator-->" , lazy_sample_Indicator)

live_csat_Indicator = channel_mean_dict["LIVECHAT"]
print("live_csat_Indicator-->" , live_csat_Indicator)
live_sample_Indicator = round((id_channel_sample_sum_dict["LIVECHAT_sum"] / id_channel_csat_count_dict["LIVECHAT_count"]/2),0)
print("live_sample_Indicator-->" , live_sample_Indicator)


# !-- channel_check DF에 Low Perfomer 체크하기
channel_check.loc[(channel_check["CALL_mean"] >= (call_csat_Indicator-0.1)) &
                  (channel_check["CALL_mean"] <= (call_csat_Indicator-0.05)) &
                  (channel_check["CALL_sum"] >= call_sample_Indicator), "CALLOUT"] = "YES"
channel_check.loc[(channel_check["LAZYCHAT_mean"] >= (lazy_csat_Indicator-0.1)) &
                  (channel_check["LAZYCHAT_mean"] <= (lazy_csat_Indicator-0.05)) &
                  (channel_check["LAZYCHAT_sum"] >= lazy_sample_Indicator), "LAZYOUT"] = "YES"
channel_check.loc[(channel_check["LIVECHAT_mean"] >= (live_csat_Indicator-0.1)) &
                  (channel_check["LIVECHAT_mean"] <= (live_csat_Indicator-0.05)) &
                  (channel_check["LIVECHAT_sum"] >= live_sample_Indicator), "LIVEOUT"] = "YES"


pd.DataFrame(channel_check).to_excel(save_locate + '상담사별 실적.xlsx', index=True)

channel_check_drop = channel_check.loc[(channel_check["CALLOUT"] == "YES") |
                        (channel_check["LAZYOUT"] == "YES") |
                        (channel_check["LIVEOUT"] == "YES")]

pd.DataFrame(channel_check_drop).to_excel(save_locate + 'Outliner LIST.xlsx', index=True)




# !-- Low Perfomer RAW 추출하기

low_Performer_ID = list(channel_check_drop.index)
print("RAW PERFORMER ID LIST \n" ,low_Performer_ID)

low_Performer_List = []

for i in low_Performer_ID:
    low_Performer_raw = workbook.loc[workbook["처리자id"] == i]
    low_Performer_List.append(low_Performer_raw)
list_merge = pd.concat(low_Performer_List, axis=0, ignore_index = True)

pd.DataFrame(list_merge).to_excel(save_locate + 'Outliner RAW.xlsx', index = False)





print("training Runtime: %0.2f Minutes"%((time.time() - start_vect)/60)) #런 타임 체크를 위해 삽입



