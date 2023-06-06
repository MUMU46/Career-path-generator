from flask import Blueprint
from flask import Flask, render_template, redirect, request, url_for
import pymysql
import spider
import json


bp = Blueprint("result", __name__, url_prefix="/")

data = {}#数据缓存

def getvideos(search):
    """使用pymysql加载首页数据"""
    # 1. 创建连接对象
    conn = pymysql.connect(host='127.0.0.1', database='Occupation',
                           user='root', password='sql_mumu')

    # 2. 创建游标对象
    cursor = conn.cursor()

    # 3. 准备SQL
    sql = 'select O_skills from Occupation where O_name LIKE "%%%s%%";' % (search)

    # 4. 执行SQL
    cursor.execute(sql)

    # 5. 获取返回数据 ((), (), ())
    result = cursor.fetchall()

    # 6. 关闭游标对象和连接对象
    cursor.close()
    conn.close()

    data_list = []
    print(result)
    for data in result:
        s1 = data[0].replace("[", "")
        s2 = s1.replace("]", "")
        s3 = s2.replace("'", "")
        s4 = s3.replace(" ", "")
        skills = s4.split(",")
        for s in skills:
            data_list.append(s)

    # 词频统计
    s = {}
    search_w = []
    for w in data_list:
        s[w] = s.get(w, 0) + 1
    l = int(len(s))  # 只返回结果出现频次靠前的几个技能
    if l <= 6:
        l = l
    elif 6 < l < 10:
        l = int(l * 0.6)
    elif 10 < l < 20:
        l = int(l * 0.3)
    else:
        l = 8

    sorted_key = sorted(s.items(), key=lambda x: x[1], reverse=True)[:l]
    print(sorted_key)

    keys = []
    for k in sorted_key:
        keys.append(k[0])
    print(keys)
    # 8. 转换为JSON字符串
    # dumps: 将Python的对象类型, 转换为JSON字符串类型
    # loads: 将JSON字符串, 转换为Python的对象类型
    # 这个dumps在调用时, 会自动转换编码为ascii编码
    jons_str = json.dumps(keys, ensure_ascii=False)
    # 传入职业名和技能数组
    videos = spider.spiderbili(search, keys)
    return videos


def month_salary(s):
    return ("K" in s) == True


def solveSalary(slist):
    new_s = filter(month_salary, slist)#过滤掉不按月发薪的数据
    s = []#月薪
    extra = []#加薪制度
    for item in new_s:
        item = item.replace("'", "")
        if "·" in item:#分割月薪和加薪制度
            l = item.split("·")
            s.append(l[0])
            extra.append(l[1])
        else:
            s.append(item)
    #判断月薪柱状图分区
    divide = {}
    for m in s:
        m = m.replace("K", "")
        m_data = m.split("-")
        if int(m_data[0]) < 10:
            divide["0-10K"] = divide.get("0-10K", 0) + 1
        if 10 < int(m_data[1]) and int(m_data[0]) < 20:
            divide["10-20K"] = divide.get("10-20K", 0) + 1
        if 20 < int(m_data[1]) and int(m_data[0]) < 30:
            divide["20-30K"] = divide.get("20-30K", 0) + 1
        if 30 < int(m_data[1]) and int(m_data[0]) < 40:
            divide["30-40K"] = divide.get("30-40K", 0) + 1
        if int(m_data[1]) > 40:
            divide["40K以上"] = divide.get("40K以上", 0) + 1
    #计算分区 0-10 10-20 20-30 30-40 40以上

    #加薪制度


    return divide


#视频页
@bp.route('/result/video/<string:search>', methods=['GET'])
def videos(search):
    global data

    if search not in data:
        videos = getvideos(search)
        # 存储数据
        data[search] = {"videos": videos}
    elif 'videos' not in data[search]:
        dic = getvideos(search)
        data[search]['videos'] = dic
    else:
        print(data)
        videos = data[search]["videos"]
    return render_template("r_video.html", videos=videos, search_w=search)


def getcharts(search, show):
    # 1. 创建连接对象
    conn = pymysql.connect(host='127.0.0.1', database='Occupation',
                           user='root', password='sql_mumu')
    # 2. 创建游标对象
    cursor = conn.cursor()

    # 3. 准备SQL
    sql = 'select %s from Occupation where O_name LIKE "%%%s%%";' % (show, search)

    # 4. 执行SQL
    cursor.execute(sql)

    # 5. 获取返回数据 ((), (), ())
    qualification = cursor.fetchall()

    # 6. 关闭游标对象和连接对象
    cursor.close()
    conn.close()

    # 数据处理
    q_list = []
    for data in qualification:
        s = data[0].replace("'", "")
        q_list.append(s)
    # 词频统计
    s = {}
    print(q_list)
    if show == 'salary':
        s = solveSalary(q_list)
    else:
        for w in q_list:
            s[w] = s.get(w, 0) + 1
    return s

#数据分析页
@bp.route('/result/charts/<string:show>/<string:search>', methods=['GET'])
def charts(show, search):
    global data

    if search not in data:
        dic = getcharts(search, show)
        #存储数据
        data[search] = {show: dic}
    elif show not in data[search]:
        dic = getcharts(search, show)
        #搜索过search值,添加show键
        data[search][show] = dic
    else:
        dic = data[search][show]
    print(dic)
    if(show == "quality"):
        if ( dic.get("博士",0)>0 ):
            m = "博士"
        elif( dic.get("硕士",0)>0):
            m = "硕士"
        elif( dic.get("本科",0)>0):
            m = "本科"
        elif( dic.get("大专",0)>0):
            m = "大专"
    elif(show == "salary"):
        if ( dic.get("40K",0)>0 ):
            m = "40K"
        elif( dic.get("30K-40K",0)>0 ):
            m = "40K"
        elif( dic.get("20-30K",0)>0 ):
            m = "30K"
        elif( dic.get("10-20K",0)>0 ):
            m = "20K"
        else:
            m = "10K"
    else:
        for key, value in dic.items():
            if(value == max(dic.values())):
                m = key
    return render_template(str("r_"+show +".html"), dict=dic, max=m, search_w=search)


#首页
@bp.route('/', methods=['GET', 'POST'])
def main():  # put application's code here
    if request.method == 'GET':
        return render_template("main.html")
    else:
        print(request.form["occu"])
        search = request.form["occu"]
        #return redirect(url_for('result.charts', show='quality', search=search))
        return redirect(url_for('result.videos', search=search))



