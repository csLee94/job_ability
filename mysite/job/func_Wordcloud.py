import pymysql 
import pandas as pd
from wordcloud import WordCloud 
from matplotlib import pyplot as plt 
import matplotlib as mpl 
import matplotlib.font_manager as fm 
import time

def make_img(code, save_path):
    mysql = pymysql.connect(host='3.34.91.54', port=55634, user='lcs', password='lcs', db='JOB', charset='utf8mb4', autocommit=True)
    cursor = mysql.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM NUM_Words WHERE code_details=%s" % code)
    data = cursor.fetchall()
    mysql.close()

    wordict = {}
    for idx in range(len(data)):
        wordict[data[idx]['word']] = data[idx]['count']


    wc = WordCloud(
        font_path = "./SCDream4.otf",
        width = 1200,
        height = 800,
        background_color = "white"
    )

    pic_array = wc.generate_from_frequencies(wordict).to_array()
    fig = plt.figure(figsize=(12,12))
    plt.imshow(pic_array, interpolation = 'bilinear')
    plt.axis('off')

    time_tuple = time.localtime()
    time_str = time.strftime("%m/%d/%Y, %H:%M:%S", time_tuple)
    # fig.savefig('./static/wordcloud_img/wci_%s_%s.png' % (str(time_str.split(', ')[0]), str(code)))
    fig.savefig(save_path+'img_%s_%s.png' % (str(code), str(time_str.split(', ')[0].replace('/', ''))))


mysql = pymysql.connect(host='3.34.91.54', port=55634, user='lcs', password='lcs', db='JOB', charset='utf8mb4', autocommit=True)
cursor = mysql.cursor(pymysql.cursors.DictCursor)
cursor.execute("SELECT * FROM Code_details")
code_data = cursor.fetchall()
code_lst = [infor['code_details'] for infor in code_data]
mysql.close()

for code in code_lst:
    try:
        make_img(code, './temp_img/')
        print("Complete: %s" % code)
    except:
        print("Failed: %s" % code)
    
