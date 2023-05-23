#-*- coding:utf-8 -*-

# 폴더 내에 포함되어 있는 여러개의 Forensic CSAT 파일에서 평가 점수만 가져오기

from pandas import Series, DataFrame
import pandas as pd
import time
import os

start_vect=time.time() #런 타임 체크를 위해 삽입

def cur_t():
    return time.strftime('%y-%m-%d-%A-%H-%M-%S',time.localtime(time.time()))



csatFile_locate = "C:/RAW_DATA/CSAT_RAW_KATE/" # 검출할 폴더 위치
csatFile_List = os.listdir(csatFile_locate)  # !---폴더 내 파일 검출
csatFile_List.sort() # 폴더 내 파일을 순차적으로 정리
csatDF_combine =[] # 빈 리스트 생성

for i in csatFile_List:
    print(i[0:30])
    if i[0:30] == "(비밀) Outsourcing CSAT raw data":
        print(i)
        workbook = pd.read_excel(csatFile_locate + i, sheet_name="CSAT raw", header=0) #엑셀 파일 내 특정 시트를 불러오기
        workbook_DF = DataFrame(workbook) # 불러온 시트를 bvhq_new 데이터 프레임으로 생성
        # workbook_DF = workbook_DF.drop(index=0)
        csatDF_combine.append(workbook_DF)
        print("작업이 진행중입니다. " ,i)
        time.sleep(1)

    else:
        print("작업을 건너뜁니다. " , i)
        continue


csat_all = pd.concat(csatDF_combine, sort=False,ignore_index=True)
csat_final = DataFrame(csat_all)


# csat_duplicated = csat_final.duplicated(["Fiscal Week", "DSID","Team Manager","Staff Type"])
#
#
# n = 0
# for i in csat_duplicated:
#     if i == True:
#         n += 1
#     else:
#         pass
#
# print(f'{n} 개의 중복을 발견했습니다.')
# csat_final = csat_final.drop_duplicates(["Fiscal Week", "DSID"])
# print(f'{n} 개의 중복을 제거했습니다.')


export_file_locate = 'C:/RAW_DATA/CSAT_RAW_KATE/' + cur_t() +'.xlsx'

csat_final.to_excel(export_file_locate)


print("training Runtime: %0.2f Minutes"%((time.time() - start_vect)/60))