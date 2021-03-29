
fpath = "C:/Users/pc1/.conda/envs/project_job/Lib/site-packages/konlpy/java/open-korean-text-2.1.0/org/openkoreantext/processor/util/noun/user.txt"


def updates(txt, path):
    add_list = add_word.split(',')
    filePath = path
    user_dict = open(filePath, 'a')
    for temptxt in add_list:
        user_dict.write(temptxt.strip('\n')+'\n')
    user_dict.close()


# 한 줄에 하나씩 ,로 끝어줄 것
add_word = '''
안녕하세요,
반갑습니다,
어서오세요,
안녕히가세요
'''
# updates(add_word)

'''
업데이트 진행 후 filepath에 가서 신규 jar 파일 생성해야 반영
> 단어 분류기 (nltk / kkma / okt) 비교 후 okt 사전에 없지만 필요한 단어들 추출하는 코드
'''

