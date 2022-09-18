import requests,xlrd,xlwt,os,webbrowser
from bs4 import BeautifulSoup

EX_RATE_KINDS=['现汇买入价',
'现钞买入价',
'现汇卖出价',
'现钞卖出价']
KINDS={'现汇买入价':0,
'现钞买入价':1,
'现汇卖出价':2,
'现钞卖出价':3}
KINDS_={0:'现汇买入价',
1:'现钞买入价',
2:'现汇卖出价',
3:'现钞卖出价'}

def check_internet_condition():
    print("----------------------------------------------------------------------")
    print("check the conection of the internet.......")
    print("----------------------------------------------------------------------")
    try:
        response=requests.get('https://www.boc.cn/sourcedb/whpj/')
    except:
        print("Error!\nPlease check your internet connection and restart the programme")
        return
    else:
        soup = BeautifulSoup(response.content.decode('utf-8'), 'lxml')
        all_exchangerate = soup.find('table',align='left',cellpadding="0")
        huilv={}
        for each_movie in all_exchangerate.find_all('tr'):
            all_td_tag=each_movie.find_all('td')
            if all_td_tag==[]:
                pass
            else:
                huilv[all_td_tag[0].text]=[all_td_tag[1].text,
                        all_td_tag[2].text,all_td_tag[3].text,
                        all_td_tag[4].text,all_td_tag[6].text]
        huilv["人民币"]=["100",'100','100','100',all_td_tag[6].text]
        return huilv

def get(currency_name=None,ex_rate_kind='现汇买入价',is_time_show=False):
    huilv=check_internet_condition()
    if not huilv:
        return
    if currency_name and ex_rate_kind:
        if is_time_show:
            return {currency_name:huilv[currency_name][KINDS[ex_rate_kind]]},huilv[currency_name][4]
        else:
            return {currency_name:huilv[currency_name][KINDS[ex_rate_kind]]},""
    elif currency_name and not ex_rate_kind:
        value={}
        for i in range(4):
            value[EX_RATE_KINDS[i]]=huilv[currency_name][i]
        if is_time_show:
            return value,huilv[currency_name][4]
        else:
            return value,""
    elif not currency_name and ex_rate_kind:
        value={}
        for i in list(huilv.keys()):
            value[i]=huilv[i][KINDS[ex_rate_kind]]
        if is_time_show:
            return value,huilv[i][4]
        else:
            return value,""
    else:
        value={}
        for i in list(huilv.keys()):
            value[i]={}
            for j in range(4):
                value[i][KINDS_[j]]=huilv[i][j]
        if is_time_show:
            return value,huilv[i][4]
        else:
            return value,""

def exchange(currency_name_1,value1,currency_name_2,ex_rate_kind='现汇买入价',is_time_show=False):
    huilv=check_internet_condition()
    if not huilv:
        return
    a=huilv[currency_name_1][KINDS[ex_rate_kind]]
    b=huilv[currency_name_2][KINDS[ex_rate_kind]]
    back=int(value1/float(b)*float(a)*1000)/1000
    if is_time_show:
        return back,huilv[currency_name_2][4]
    else:
        return back,""

def help(language="Chinese"):
    pass

huilv=check_internet_condition()
print(huilv.keys())
# print(exchange("人民币",120,"美元",is_time_show=True))
# get.you(huilv)
# 增加容错率（参数）