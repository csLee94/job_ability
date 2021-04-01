import pymysql 
import pandas as pd
from wordcloud import WordCloud 
from matplotlib import pyplot as plt 
import matplotlib as mpl 
import matplotlib.font_manager as fm 
import time

def make_img(code):
    mysql = pymysql.connect(host='3.34.133.199', port=58215, user='lcs', password='lcs', db='JOB', charset='utf8mb4', autocommit=True)
    cursor = mysql.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM Code_details WHERE code_details=%s" % code)
    code_name = cursor.fetchall()
    code_name = code_name[0]['name_details']
    cursor.execute("SELECT * FROM NUM_Words WHERE code_details=%s" % code)
    data = cursor.fetchall()
    mysql.close()

    wordict = {}
    for idx in range(len(data)):
        wordict[data[idx]['word']] = data[idx]['count']
    wc = WordCloud(
        font_path = "job/static/Font/SCDream4.otf",
        width = 1200,
        height = 800,
        background_color = "white"
    )

    pic_array = wc.generate_from_frequencies(wordict).to_array()
    fig = plt.figure(figsize=(12,8))
    plt.imshow(pic_array, interpolation = 'bilinear')
    plt.axis('off')

    time_tuple = time.localtime()
    time_str = time.strftime("%m/%d/%Y, %H:%M:%S", time_tuple)
    fig.savefig('job/static/show_img/img_%s_%s.png' % (str(code), str(time_str.split(', ')[0].replace('/', ''))))
    name = str('img_%s_%s.png' % (str(code), str(time_str.split(', ')[0].replace('/', ''))))
    plt.cla()
    path = "job/static/Font/SCDream4.otf"
    font = fm.FontProperties(fname=path).get_name()
    plt.rc('font', family = font)
    fig = plt.figure(figsize=(10,6))
    plt.bar(list(wordict.keys())[:20], list(wordict.values())[:20])
    plt.savefig('job/static/show_img/chart_%s_%s.png' % (str(code), str(time_str.split(', ')[0].replace('/', ''))))
    chart_name = str('chart_%s_%s.png' % (str(code), str(time_str.split(', ')[0].replace('/', ''))))

    return name, code_name, chart_name


