# 爬取新冠状病毒数据并绘制地图
# -*- coding: utf-8 -*-
import time, json, requests, warnings
import pandas as pd
from pyecharts.charts import Map
import pyecharts.options as opts
warnings.filterwarnings("ignore")
# 抓取腾讯疫情实时json数据
url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d'%int(time.time()*1000)
data = json.loads(requests.get(url=url).json()['data'])
# 统计省份信息(34个省份 湖北 广东 河南 浙江 湖南 安徽....)
num = data['areaTree'][0]['children']
# 解析确诊数据
total_data = {}
for item in num:
    if item['name'] not in total_data:
        total_data.update({item['name']:0})
    for city_data in item['children']:
        total_data[item['name']] +=int(city_data['total']['confirm'])
# 解析疑似数据
total_suspect_data = {}
for item in num:
    if item['name'] not in total_suspect_data:
        total_suspect_data.update({item['name']:0})
    for city_data in item['children']:
        total_suspect_data[item['name']] +=int(city_data['total']['suspect'])
# 解析死亡数据
total_dead_data = {}
for item in num:
    if item['name'] not in total_dead_data:
        total_dead_data.update({item['name']:0})
    for city_data in item['children']:
        total_dead_data[item['name']] +=int(city_data['total']['dead'])
# 解析治愈数据
total_heal_data = {}
for item in num:
    if item['name'] not in total_heal_data:
        total_heal_data.update({item['name']:0})
    for city_data in item['children']:
        total_heal_data[item['name']] +=int(city_data['total']['heal'])
# 解析新增确诊数据
total_new_data = {}
for item in num:
    if item['name'] not in total_new_data:
        total_new_data.update({item['name']:0})
    for city_data in item['children']:
        total_new_data[item['name']] +=int(city_data['today']['confirm']) # today
names = list(total_data.keys())          # 省份名称
num1 = list(total_data.values())         # 确诊数据
num2 = list(total_suspect_data.values()) # 疑似数据(全为0)
num3 = list(total_dead_data.values())    # 死亡数据
num4 = list(total_heal_data.values())    # 治愈数据
num5 = list(total_new_data.values())     # 新增确诊病例
# 获取当前日期命名(2020-02-13-all.csv)
n = "新冠状病毒实时疫情地图-" + time.strftime("%Y-%mm-%dd") + ".csv"
fw = open(n, 'w', encoding='utf-8')
fw.write('province,confirm,dead,heal,new_confirm\n')
i = 0
while i<len(names):
    fw.write(names[i]+','+str(num1[i])+','+str(num3[i])+','+str(num4[i])+','+str(num5[i])+'\n')
    i = i + 1
else:
    print("Over write file!")
    fw.close()
# 读取数据
n = "新冠状病毒实时疫情地图-" + time.strftime("%Y-%mm-%dd") + ".csv"
data = pd.read_csv(n)
list_data = list(zip(data['province'], data['confirm'])) #Python3 Print zip，需在zip前加list
def map_disease_dis() -> Map:
    c = (
        Map()
        .add('中国', list_data, 'china')
        .set_global_opts(
            title_opts=opts.TitleOpts(title='全国新型冠状病毒疫情地图（确诊数）'),
            visualmap_opts=opts.VisualMapOpts(is_show=True,
                                              split_number=6,
                                              is_piecewise=True,  # 是否为分段型
                                              pos_top='center',
                                              pieces=[
                                                   {'min': 10000, 'color': '#7f1818'},  #不指定 max
                                                   {'min': 1000, 'max': 10000},
                                                   {'min': 500, 'max': 999},
                                                   {'min': 100, 'max': 499},
                                                   {'min': 10, 'max': 99},
                                                   {'min': 0, 'max': 5} ],
                                              ),
        )
    )
    return c
map_disease_dis().render('全国新冠状病毒实时疫情地图.html')

# 获取四川省下标及各城市
k = 0
for item in num:
    if item['name'] in "四川":
        break
    k = k + 1
sc = num[k]['children']
total_data = {}
for item in sc:
    # 补齐城市名称
    item['name'] = item['name'] + '市'
    if item['name'] in '阿坝市':
       item['name'] = '阿坝藏族羌族自治州'
    if item['name'] in '甘孜市':
       item['name'] = '甘孜藏族自治州'
    if item['name'] in '凉山市':
       item['name'] = '凉山彝族自治州'
    if item['name'] not in total_data:
        total_data.update({item['name']:0})
    total_data[item['name']] = item['total']['confirm']
list_data = zip(total_data.keys(),total_data.values())
def map_disease_dis() -> Map:
    c = (
        Map()
        .add('四川省', list_data, '四川')
        .set_global_opts(
                    title_opts=opts.TitleOpts(title='四川省新型冠状病毒疫情地图（确诊数）'),
                    visualmap_opts=opts.VisualMapOpts(is_show=True,
                                                      split_number=6,
                                                      is_piecewise=True,  # 是否为分段型
                                                      pos_top='center',
                                                      pieces=[
                                                           {'min': 50},
                                                           {'min': 30, 'max': 49},
                                                           {'min': 20, 'max': 29},
                                                           {'min': 10, 'max': 19},
                                                           {'min': 1, 'max': 9},
                                                           {'value': 0, "label": '无确诊病例', "color": 'green'} ],
                                                      ),
                )
    )
    return c
map_disease_dis().render('四川省疫情地图.html')