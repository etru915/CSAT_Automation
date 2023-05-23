from konlpy.tag import Okt
from collections import Counter

tokenizer = Okt()



file = open('C:\\Users\\zeno915\\Desktop\\text_raw.txt','rt' , encoding='UTF8')
lines = file.read()

noun = tokenizer.nouns(lines)

print(Counter(noun))