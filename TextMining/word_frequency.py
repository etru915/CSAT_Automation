from konlpy.tag import Kkma

kkma = Kkma()

para = " 형태소 분석을 시작합니다. 나는 홍길동이고, age는 28 세 입니다."

ex_sent=kkma.sentences(para)

print(ex_sent)