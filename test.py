import pandas as pd


df = pd.read_excel("C:\\Users\\zeno915\\Desktop\\upload_list.xlsx" ,sheet_name= 'Sheet1', header=0,usecols="b:e",index_col= 'no',encoding='utf-8')
df = df[df['Action y/n'] == 0]
df = df.reset_index(drop=True)
# df.index.name = 'no'

print(df['macro_title'][0])