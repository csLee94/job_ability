from django.shortcuts import render
# from django.http import HttpResponse
from .func_Wordcloud import make_img
# Create your views here.

# def home(request):
#     data = request.GET.copy()
#     result_data= dict()
#     if 'select' in data.keys():
#         scode = change(data['select'])
#         result_data['name'] = make_img(scode)
#     return render(request, 'job/home.html', context=result_data)

def home(request):
    data = request.GET.copy()
    result_data= dict()
    if 'select' in data.keys():
        scode = change(data['select'])
        result_data['name'], result_data['code_name'], result_data['chart_name'] = make_img(scode)
        return render(request, 'job/img_show.html', context=result_data)
    else:
        return render(request, 'job/home.html')

def change(value):
    codict = {
        "1": "872",
        "2": "873",
        "3": "669",
        "4": "660",
        "5": "677",
        "6": "678",
        "7": "899",
        "8": "655",
        "9": "674",
        "10": "895",
        "11": "900",
        "12": "1634",
        "13": "665",
        "14": "1024",
        "15": "877",
        "16": "565",
        "17": "564",
        "18": "559",
        "19": "563",
        "20": "554",
        "21": "656",
        "22": "552",
        "23": "1030",
        "24": "710",
        "25": "719",
        "26": "1635",
        "27": "707",
        "28": "721",
        "29": "717",
        "30": "599",
        "31": "597",
        "32": "594",
        "33": "592",
        "34": "595",
        "35": "603",
        "36": "879",
        "37": "1036",
        "38": "770",
        "39": "954",
        "40": "766",
        "41": "768",
        "42": "1035",
        "43": "955",
        "44": "1028",
        "45": "758",
        "46": "586",
        "47": "760",
        "48": "901",
        "49": "769",
        "50": "754",
        "51": "1046",
        "52": "723",
        "53": "727",
        "54": "725",
        "55": "3351",
        "56": "724",
        "57": "957",
        "58": "643",
        "59": "649",
        "60": "644",
        "61": "648",
        "62": "645",
        "63": "1043",
        "64": "647",
        "65": "1048",
        "66": "538",
        "67": "534",
        "68": "920",
        "69": "542",
        "70": "1047",
        "71": "882",
        "72": "822",
        "73": "823",
        "74": "821",
        "75": "843",
        "76": "856",
        "77": "859",
        "78": "817",
        "79": "959",
        "80": "515",
        "81": "522",
        "82": "532",
        "83": "10057",
        "84": "521",
        "85": "509",
        "86": "514"
    }
    scode = codict[value]
    return scode