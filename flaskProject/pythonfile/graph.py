from pyecharts.charts import Page, Radar, Funnel
from pyecharts.globals import ThemeType
from sqlalchemy import create_engine
import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import WordCloud
from pyecharts.charts import Pie



def get_data(y):
    stop = ['and', 'the', '抽烟', '打手机', '本科教务管理', '个人简介', '新加坡', '美国', 'to', 'for', 'our', 'us', '(the', 'a', '1.', '2.',
            '3.', 'The', 'is', 'be', 'or', 'has', 'it', 'In', 'my', 'from', 'that', 'PhD', 'china', 'of', 'in', 'My',
            'We', 'also', 'can', 'interested', 'such', 'are', 'as', 'am', 'this', 'on', 'out','/']
    count={}
    for i in y:
        try:
            for j in i:
#                 print(j)
                if j in stop:
                    continue
                if j not in count:
                    count[j]=0
                count[j]=count[j]+1
        except:
            continue
    data=list(count.items())
    return data

def pie(y,args):

    x_data = list(args.keys())
    y_data = list(args.values())
    data_pair = [list(z) for z in zip(x_data, y_data)]
    data_pair.sort(key=lambda x: x[1])
    return (
        Pie(init_opts=opts.InitOpts(width='650px', height='500px',theme=ThemeType.VINTAGE))
            .add(
            "",
            [list(z) for z in zip(x_data, y_data)],
            radius=["40%", "55%"],
            label_opts=opts.LabelOpts(
                position="outside",
                formatter="{b|{b}: }{c}  {per|{d}%}  ",
                background_color="#eee",
                border_color="#aaa",
                border_width=1,
                border_radius=2,
                rich={

                    "b": {"fontSize": 10, "lineHeight": 20},
                    "per": {
                        "color": "#eee",
                        "backgroundColor": "#334455",
                        "padding": [0,0],
                        "borderRadius": 0,
                    },
                },
            )
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="专业-导师数量分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23),pos_top='0px',pos_left='300px'),
            tooltip_opts=opts.TooltipOpts(is_show=True),
            legend_opts=opts.LegendOpts(is_show=False)
        )
            # .render("./pie_rich_label.html")
    )

def radar(y,args):
    v1 = [list(args.values())]
    schema = []
    max_ = 1000
    for x in list(args.keys()):
        schema.append(opts.RadarIndicatorItem(name=x, max_=15))
    return (
        Radar(init_opts=opts.InitOpts(width='650px', height='500px',theme=ThemeType.VINTAGE))
            .add_schema(
            schema=schema
        )
            .add("统计", v1)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            legend_opts=opts.LegendOpts(selected_mode="single"),
            title_opts=opts.TitleOpts(title="专业分析雷达图", title_textstyle_opts=opts.TextStyleOpts(font_size=23),pos_top='0px',pos_left='250px')
        )
            # .render("./专业分析雷达图.html")
    )

def loudou(y,args):
    return (
        Funnel(init_opts=opts.InitOpts(width='650px', height='500px',theme=ThemeType.VINTAGE))
            .add(
            "领域-人数",
            [list(z) for z in zip(list(args.keys()), list(args.values()))],
            sort_="ascending"
            #         label_opts=opts.LabelOpts(position="inside"),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="专业分析漏斗图", title_textstyle_opts=opts.TextStyleOpts(font_size=23),pos_top='0px',pos_left='250px'),
                             legend_opts=opts.LegendOpts(is_show=False))
            # .render("./funnel_sort_ascending.html")
    )
def wordcloud(y,args):
    return (
        WordCloud(init_opts=opts.InitOpts(width='650px', height='500px',theme=ThemeType.VINTAGE))
            .add(series_name="专业词云分析", data_pair=get_data(y), word_size_range=[30, 60],pos_left='150px')
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="专业词云分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23),pos_left='300px'),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
    )


engine = create_engine(
        "mysql+pymysql://{}:{}@{}/{}?charset={}".format('root', 'welcome2019', '127.0.0.1:3306', 'webdataofteachers',
                                                        'utf8mb4'))
sql = '''
        select * from teachers
      '''
df = pd.read_sql_query(sql, engine)

# df['email']=df['email'].replace('NaN',"")
zju = df[df['email'].str.contains("zju", na=False)]
sjt = df[df['email'].str.contains("sjtu", na=False)]
hust = df[df['email'].str.contains("hust", na=False)]
ict = df[df['email'].str.contains("ict\.ac", na=False)]
ia = df[df['email'].str.contains("ia\.ac", na=False)]
shanghaitech = df[df['email'].str.contains("shanghaitech", na=False)]
fudan = df[df['email'].str.contains("fudan", na=False)]


def zju_page():
    zju['workfield'] = zju['workfield'].str.strip()
    zju_y = list(zju['workfield'].str.split(' '))
    word_list = get_data(zju_y)
    zju_args = {}
    for item in word_list:
        if item[1] >= 3:
            zju_args[item[0]] = item[1]
    page=Page(layout=Page.SimplePageLayout)
    page.add(loudou(zju_y,zju_args),radar(zju_y,zju_args),wordcloud(zju_y,zju_args),pie(zju_y,zju_args))
    return page

def hust_page():
    hust['workfield'] = hust['workfield'].str.strip()
    hust_y = list(hust['workfield'].str.split(' '))
    word_list = get_data(hust_y)
    hust_args = {}
    for item in word_list:
        if item[1] >=2:
            hust_args[item[0]] = item[1]
    page=Page(layout=Page.SimplePageLayout)
    page.add(wordcloud(hust_y,hust_args),pie(hust_y,hust_args),loudou(hust_y,hust_args),radar(hust_y,hust_args))
    return page

def ict_page():
    ict['workfield'] = ict['workfield'].str.strip()
    ict_y = list(ict['workfield'].str.split(' '))
    word_list = get_data(ict_y)
    ict_args = {}
    for item in word_list:
        if item[1] >=3:
            ict_args[item[0]] = item[1]
    page=Page(layout=Page.SimplePageLayout)
    page.add(wordcloud(ict_y,ict_args),pie(ict_y,ict_args),loudou(ict_y,ict_args),radar(ict_y,ict_args))
    return page

def ia_page():
    ia['workfield'] = ia['workfield'].str.strip()
    ia_y = list(ia['workfield'].str.split(' '))
    word_list = get_data(ia_y)
    ia_args = {}
    for item in word_list:
        if item[0]=="IEEE" or item[0]=="":
            continue
        if item[1] >=5:
            ia_args[item[0]] = item[1]
    page=Page(layout=Page.SimplePageLayout)
    page.add(wordcloud(ia_y,ia_args),pie(ia_y,ia_args),loudou(ia_y,ia_args),radar(ia_y,ia_args))
    return page

def shanghaitech_page():
    shanghaitech['workfield'] = shanghaitech['workfield'].str.strip()
    shanghaitech_y = list(shanghaitech['workfield'].str.split(' '))
    word_list = get_data(shanghaitech_y)
    shanghaitech_args = {}
    for item in word_list:
        if item[0]=="IEEE" or item[0]=="":
            continue
        if item[1] >=2:
            shanghaitech_args[item[0]] = item[1]
    page=Page(layout=Page.SimplePageLayout)
    page.add(wordcloud(shanghaitech_y,shanghaitech_args),pie(shanghaitech_y,shanghaitech_args),loudou(shanghaitech_y,shanghaitech_args),radar(shanghaitech_y,shanghaitech_args))
    return page

def fudan_page():
    fudan['workfield'] = fudan['workfield'].str.strip()
    fudan_y = list(fudan['workfield'].str.split(' '))
    word_list = get_data(fudan_y)
    fudan_args = {}
    for item in word_list:
        if item[0]=="IEEE":
            continue
        if item[1] >=2:
            fudan_args[item[0]] = item[1]
    page=Page(layout=Page.SimplePageLayout)
    page.add(wordcloud(fudan_y,fudan_args),pie(fudan_y,fudan_args),loudou(fudan_y,fudan_args),radar(fudan_y,fudan_args))
    return page