import pandas as pd
import time


start_vect=time.time() #런 타임 체크를 위해 삽입

# file_locate = "C:/Users/zeno915/Desktop/CSAT_Raw_Refine.xlsx"
file_locate = "C:/Users/zeno915/Desktop/SQL_TEST_02.xlsx"

df = pd.read_excel(file_locate, sheet_name='Sheet1',index_col="설문번호", header= 0)
df_agent_merge = []

# CSAT 합계 구하기
df_agent = pd.pivot_table(df, index="처리자id", columns="상담경로", values="CSAT_B", aggfunc="sum")
df_agent_csat_sum = pd.DataFrame(df_agent)
df_agent_csat_sum.rename(columns = {'CALL' : 'CALL_CSAT_sum','LAZYCHAT':'LAZYCHAT_CSAT_sum','LIVECHAT':'LIVECHAT_CSAT_sum'}, inplace = True)
df_agent_merge.append(df_agent_csat_sum)

# Survey 합계 구하기
df_agent = pd.pivot_table(df, index="처리자id", columns="상담경로", values="CSAT_B", aggfunc="count")
df_agent_survey_count = pd.DataFrame(df_agent)
df_agent_survey_count.rename(columns = {'CALL' : 'CALL_Survey_count','LAZYCHAT':'LAZYCHAT_Survey_count','LIVECHAT':'LIVECHAT_Survey_count'}, inplace = True)
df_agent_merge.append(df_agent_survey_count)

# VD 합계 구하기
df_agent = pd.pivot_table(df, index="처리자id", columns="상담경로", values="CSAT_VD", aggfunc="sum")
df_agent_VD_count = pd.DataFrame(df_agent)
df_agent_VD_count.rename(columns = {'CALL' : 'CALL_VD_count','LAZYCHAT':'LAZYCHAT_VD_count','LIVECHAT':'LIVECHAT_VD_count'}, inplace = True)
df_agent_merge.append(df_agent_VD_count)

# AR 합계 구하기
df_agent = pd.pivot_table(df, index="처리자id", columns="상담경로", values="불만원인_B", aggfunc="sum")
df_agent_AR_count = pd.DataFrame(df_agent)
df_agent_AR_count.rename(columns = {'CALL' : 'CALL_AR_count','LAZYCHAT':'LAZYCHAT_AR_count','LIVECHAT':'LIVECHAT_AR_count'}, inplace = True)
df_agent_merge.append(df_agent_AR_count)

# 불친절 합계 구하기
df_agent = pd.pivot_table(df, index="처리자id", columns="상담경로", values="불친절", aggfunc="sum")
df_agent_lackofkind_count = pd.DataFrame(df_agent)
df_agent_lackofkind_count.rename(columns = {'CALL' : 'CALL_불친절_count','LAZYCHAT':'LAZYCHAT_불친절_count','LIVECHAT':'LIVECHAT_불친절_count'}, inplace = True)
df_agent_merge.append(df_agent_lackofkind_count)

# 응대불만 합계 구하기
df_agent = pd.pivot_table(df, index="처리자id", columns="상담경로", values="응대불만", aggfunc="sum")
df_agent_lackofdeal_count = pd.DataFrame(df_agent)
df_agent_lackofdeal_count.rename(columns = {'CALL' : 'CALL_응대불만_count','LAZYCHAT':'LAZYCHAT_응대불만_count','LIVECHAT':'LIVECHAT_응대불만_count'}, inplace = True)
df_agent_merge.append(df_agent_lackofdeal_count)

# 설명부족 합계 구하기
df_agent = pd.pivot_table(df, index="처리자id", columns="상담경로", values="설명부족", aggfunc="sum")
df_agent_lackofexplain_count = pd.DataFrame(df_agent)
df_agent_lackofexplain_count.rename(columns = {'CALL' : 'CALL_설명부족_count','LAZYCHAT':'LAZYCHAT_설명부족_count','LIVECHAT':'LIVECHAT_설명부족_count'}, inplace = True)
df_agent_merge.append(df_agent_lackofexplain_count)

df_agent_all = pd.concat(df_agent_merge, axis=1)


df_agent_all["CALL_CSAT_Rate"] = df_agent_all["CALL_CSAT_sum"] / df_agent_all["CALL_Survey_count"]
df_agent_all["CALL_AR_Rate"] = df_agent_all["CALL_AR_count"] / df_agent_all["CALL_Survey_count"]
df_agent_all["CALL_불친절_Rate"] = df_agent_all["CALL_불친절_count"] / df_agent_all["CALL_Survey_count"]
df_agent_all["CALL_응대불만_Rate"] = df_agent_all["CALL_응대불만_count"] / df_agent_all["CALL_Survey_count"]
df_agent_all["CALL_설명부족_Rate"] = df_agent_all["CALL_설명부족_count"] / df_agent_all["CALL_Survey_count"]

df_agent_all["LAZYCHAT_CSAT_Rate"] = df_agent_all["LAZYCHAT_CSAT_sum"] / df_agent_all["LAZYCHAT_Survey_count"]
df_agent_all["LAZYCHAT_AR_Rate"] = df_agent_all["LAZYCHAT_AR_count"] / df_agent_all["LAZYCHAT_Survey_count"]
df_agent_all["LAZYCHAT_불친절_Rate"] = df_agent_all["LAZYCHAT_불친절_count"] / df_agent_all["LAZYCHAT_Survey_count"]
df_agent_all["LAZYCHAT_응대불만_Rate"] = df_agent_all["LAZYCHAT_응대불만_count"] / df_agent_all["LAZYCHAT_Survey_count"]
df_agent_all["LAZYCHAT_설명부족_Rate"] = df_agent_all["LAZYCHAT_설명부족_count"] / df_agent_all["LAZYCHAT_Survey_count"]

df_agent_all["LIVECHAT_CSAT_Rate"] = df_agent_all["LIVECHAT_CSAT_sum"] / df_agent_all["LIVECHAT_Survey_count"]
df_agent_all["LIVECHAT_AR_Rate"] = df_agent_all["LIVECHAT_AR_count"] / df_agent_all["LIVECHAT_Survey_count"]
df_agent_all["LIVECHAT_불친절_Rate"] = df_agent_all["LIVECHAT_불친절_count"] / df_agent_all["LIVECHAT_Survey_count"]
df_agent_all["LIVECHAT_응대불만_Rate"] = df_agent_all["LIVECHAT_응대불만_count"] / df_agent_all["LIVECHAT_Survey_count"]
df_agent_all["LIVECHAT_설명부족_Rate"] = df_agent_all["LIVECHAT_설명부족_count"] / df_agent_all["LIVECHAT_Survey_count"]


header_list = ['LP_ALL', 'LP_CALL', 'LP_LIVE', 'LP_LAZY',
               'CALL_CSAT_sum', 'CALL_Survey_count', 'CALL_CSAT_Rate', 'CALL_AR_count', 'CALL_AR_Rate',
               'CALL_VD_count', 'CALL_불친절_count', 'CALL_불친절_Rate', 'CALL_설명부족_count', 'CALL_설명부족_Rate',
               'CALL_응대불만_count', 'CALL_응대불만_Rate',
               'LIVECHAT_CSAT_sum', 'LIVECHAT_Survey_count', 'LIVECHAT_CSAT_Rate', 'LIVECHAT_AR_count', 'LIVECHAT_AR_Rate',
               'LIVECHAT_VD_count', 'LIVECHAT_불친절_count', 'LIVECHAT_불친절_Rate', 'LIVECHAT_설명부족_count', 'LIVECHAT_설명부족_Rate',
               'LIVECHAT_응대불만_count', 'LIVECHAT_응대불만_Rate',
               'LAZYCHAT_CSAT_sum', 'LAZYCHAT_Survey_count', 'LAZYCHAT_CSAT_Rate', 'LAZYCHAT_AR_count', 'LAZYCHAT_AR_Rate',
               'LAZYCHAT_VD_count', 'LAZYCHAT_불친절_count', 'LAZYCHAT_불친절_Rate', 'LAZYCHAT_설명부족_count', 'LAZYCHAT_설명부족_Rate',
               'LAZYCHAT_응대불만_count', 'LAZYCHAT_응대불만_Rate']

df_agent_all = pd.DataFrame(df_agent_all , columns= header_list)
# multi_check = pd.pivot_table(multi_checker,index = ["처리자id","wk"] , columns= "상담경로" , values="IC_Month" ,aggfunc= "count" )
print(df_agent_all.columns)

call_avg = 0.82
call_VD = 1
live_avg = 0.82
live_VD = 1
lazy_avg = 0.82
lazy_VD = 1

df_agent_all.loc[(df_agent_all["CALL_CSAT_Rate"] < call_avg) & (df_agent_all["CALL_VD_count"] > call_VD) , "LP_CALL"] = "대상"
df_agent_all.loc[(df_agent_all["LIVECHAT_CSAT_Rate"] < live_avg) & (df_agent_all["LIVECHAT_VD_count"] > live_VD) , "LP_LIVE"] = "대상"
df_agent_all.loc[(df_agent_all["LAZYCHAT_CSAT_Rate"] < lazy_avg) & (df_agent_all["LAZYCHAT_VD_count"] > lazy_VD) , "LP_LAZY"] = "대상"
df_agent_all.loc[(df_agent_all["LP_CALL"]=="대상") | (df_agent_all["LP_LIVE"] =="대상") | (df_agent_all["LP_LAZY"] =="대상"), "LP_ALL"] = "대상"


df_agent_all.to_excel("C:/Users/zeno915/Desktop/Agent_Raw_create.xlsx", encoding="EUC-KR")


print("training Runtime: %0.2f Minutes"%((time.time() - start_vect)/60)) #런 타임 체크를 위해 삽입

# 해야할 일 - 멀티 지원 상담사 구분하기 / agent_all에 CSAO	Location 삽입하는 방법 구상
# 전체 보고서 만들기
# memberid / 상담완료 시간 전체적으로 추가하기 (Ring 검색을 위해)
