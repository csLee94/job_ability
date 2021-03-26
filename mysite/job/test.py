import re

def del_korean(text):
    txt = text 
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
    result=hangul.findall(txt)
    return result


txt = [
    "ERP프로그램",
    "Python개발",
    "실사Finace",
    "한글말로"
]


for t in txt:
    print(len(del_korean(t)))