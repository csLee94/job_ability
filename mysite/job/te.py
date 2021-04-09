import pymysql 
import pandas as pd
from wordcloud import WordCloud 
from matplotlib import pyplot as plt 
import matplotlib as mpl 
import matplotlib.font_manager as fm 
import time

# def make_img(code):
#     font_fname = "./static/Font/SCDream4.otf"
#     font_family = fm.FontProperties(fname=font_fname).get_name()
#     plt.rcParams["font.family"] = font_family
#     fig2, ax2 = plt.subplots()

#     mysql = pymysql.connect(host='3.35.149.226', port=59757, user='lcs', password='lcs', db='JOB', charset='utf8mb4', autocommit=True)
#     cursor = mysql.cursor(pymysql.cursors.DictCursor)
#     cursor.execute("SELECT * FROM Code_details WHERE code_details=%s" % code)
#     code_name = cursor.fetchall()
#     code_name = code_name[0]['name_details']
#     cursor.execute("SELECT * FROM NUM_Words WHERE code_details=%s" % code)
#     data = cursor.fetchall()
#     mysql.close()

#     wordict = {}
#     for idx in range(len(data)):
#         wordict[data[idx]['word']] = data[idx]['count']
#     wc = WordCloud(
#         font_path = font_fname,
#         width = 1200,
#         height = 800,
#         background_color = "white"
#     )

#     pic_array = wc.generate_from_frequencies(wordict).to_array()
#     fig = plt.figure(figsize=(12,8))
#     plt.imshow(pic_array, interpolation = 'bilinear')
#     plt.axis('off')

#     time_tuple = time.localtime()
#     time_str = time.strftime("%m/%d/%Y, %H:%M:%S", time_tuple)
#     fig.savefig('./img_%s_%s.png' % (str(code), str(time_str.split(', ')[0].replace('/', ''))))
#     name = str('img_%s_%s.png' % (str(code), str(time_str.split(', ')[0].replace('/', ''))))
#     plt.close()

#     ax2.bar(list(wordict.keys())[:20], list(wordict.values())[:20])
#     fig2.savefig('./chart_%s_%s.png' % (str(code), str(time_str.split(', ')[0].replace('/', ''))))

#     # fig = plt.figure(figsize=(10,6))
#     # plt.bar(list(wordict.keys())[:20], list(wordict.values())[:20])
#     # plt.savefig('./chart_%s_%s.png' % (str(code), str(time_str.split(', ')[0].replace('/', ''))))
#     chart_name = str('chart_%s_%s.png' % (str(code), str(time_str.split(', ')[0].replace('/', ''))))

# make_img('10056')

tempdict = {'가':10, '나':20, '다':30}
font_fname = "./static/Font/SCDream4.otf"
font_family = fm.FontProperties(fname=font_fname)
fig, ax = plt.subplots()

# ax.axis(list(tempdict.keys()), list(tempdict.values()), fontproperties=font_family)

ax.bar(list(tempdict.keys())[:20], list(tempdict.values())[:20])
# fig.xlabel(list(tempdict.keys())[:20], fontproperties=font_family)
fig.figsave('./temp.png')