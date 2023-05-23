import pandas as pd
import time
import Low_Performer_Extractor._1_CSAT_Raw_Extractor


start_vect=time.time() #런 타임 체크를 위해 삽입

file_locate = "C:/Users/zeno915/Desktop/pycharm/CSAT_Raw_Extractor.xlsx"

header_list = ['상담경로','상담조직','상담센터','site','처리자id','문의유형대','문의유형중','문의유형소','상품유형',
                 '상담번호','csat_5points','연결지연','불친절','응대불만','설명부족','처리지연','기타','근속주','구분','skilled구분',
               'cate1','cate2','cate3','cate4','상담완료일시','설문종료일시','yyyy_wk기준','wk']

df = pd.read_excel(file_locate,sheet_name='Sheet1',index_col= "설문번호" , header= 0)

df = pd.DataFrame(df, columns=header_list)

# !---- 추가열 생성 부분

df["IC_Month"] = df["설문종료일시"].dt.month

df["IC_Day"] = df["설문종료일시"].dt.day

df["IC_Weekday"] = df["설문종료일시"].dt.dayofweek

df["IC_Weekend"] = df["IC_Weekday"].apply(lambda x: 1 if x == 5 or x == 6 else 0)

df["IC_Hour"] = df["설문종료일시"].dt.hour

df['CH_처리자ID'] = df["상담센터"].apply(lambda x: str(x)[0:1]) + "_" + \
                    df["상담경로"].apply(lambda x: str(x)[0:2]) + "_" + \
                    df["처리자id"]

df["CSAT_B"] = df["csat_5points"].apply(lambda x: 1 if x >= 4 else 0)

df["CSAT_VD"] = df["csat_5points"].apply(lambda x: 1 if x == 1 else None)

df["Center_B"] = df["상담센터"].apply(lambda x: x if x == "KBSJOB" or x == "TCK" or x == "U-BASE" else "CSA")

df["만족도"] = df['csat_5points'].apply(lambda x: "5_매우만족" if x == 5 else "4_다소만족" if x == 4 else "3_보통불만" if x == 3 else "2_다소불만" if x == 2 else "1_매우불만")

df["불만원인"] = df["불친절"] + df["응대불만"] + df["설명부족"]
df["불만원인"] = df["불만원인"].apply(lambda x: "상담사" if x >= 1 else "기타")
df["불만원인_B"] = df["불만원인"].apply(lambda x: 1 if x == "상담사" else 0)

df["만족도/불만원인"] = df["만족도"] + "_" + df["불만원인"]

df.to_excel("C:/Users/zeno915/Desktop/pycharm/CSAT_Raw_Refine.xlsx", encoding="EUC-KR")
print("파일 저장을 완료하였습니다.")

print("training Runtime: %0.2f Minutes"%((time.time() - start_vect)/60)) #런 타임 체크를 위해 삽입