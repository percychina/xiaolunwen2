from pygeohash import encode, decode
import plotly
import numpy as np
import pandas as pd
import math
from matplotlib.path import Path
import numpy as np
import plotly.offline as of
import plotly.graph_objs as go
import chart_studio.plotly as py
import numpy as np
import pandas as pd
import folium
import webbrowser
from folium.plugins import HeatMap
import datetime
import time
import pymysql.cursors
import decimal
import geohash
def geohashsql(geohash):
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='xu19931026',
        db='cd_taxi',
        charset='utf8'
    )
    if conn:
        print("2次连接成功!")
    geohash=(" ".join(geohash)) #列表转换为字符串
    cursor = conn.cursor()  # 获取游标
    sql = "UPDATE Order_Data SET geo=%s WHERE id=%s"  # sql语句
    cursor.execute(sql,(geohash,id))
    conn.commit() #不加这一句不执行
    conn.close()  # 关闭数据库连接


def mysql():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='xu19931026',
        db='cd_taxi',
        charset='utf8'
    )
    if conn:
        print("连接成功!")

    cursor = conn.cursor()  # 获取游标
    sql = "select CAST(BeginLongitude as CHAR(11)) as BeginLongitude,CAST(BeginLatitude as CHAR(10)) as BeginLatitude FROM Order_Data where id=%s"  # sql语句
    cursor.execute(sql,id)

    result=cursor.fetchall()
    df=list(result)  #将元组转换为列表
    lon = []
    lat = []
    conn.close()#关闭数据库连接
    for point in df:
        lon.append(float(point[0]))  #将字符串的经纬度转换为float格式
        lat.append(float(point[1]))
    return lon,lat
def get_lonandlat(geo):
    lat, lon = geohash.decode(geo)  # precision=9可以加精度
    return lat, lon
def get_geohash(lon, lat):
    #生成Geohash
    geo = geohash.encode(lat, lon)  # precision=9可以加精度
    return geo
def get_geolist(lon,lat):  #根据MySQL出的经纬度生成Geohash
    p = []
    for i in range(len(lon)):
        result = get_geohash(lon[i],lat[i])
        p.append(result)
    return p
def top_geohash(geohash1,n):
    new_total = []  # 根据total 得到的前4位全部的编码
    block_dict = {}
    central_dict = {}
    for i in geohash1:
        new_total.append(i[:n])  # 取前n个geohash
    return new_total  #存放所有的Geohash并根据前4位Geohash编码解析出新经纬度


if __name__ == "__main__":
    id = 430455
    while id < 645105:
        lon,lat=mysql() # 获取MySQL里的经度，纬度，经度纬度组成的列表
        geohash1=get_geolist(lon,lat) # 根据经纬度获得geohash1列表
        geohashsql(geohash1)
        id += 1
        print(id-1)
    print('处理完毕')

    # geohash2=top_geohash(geohash1,5) # geohash2为geohash1的前n位
