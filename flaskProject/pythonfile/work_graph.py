from pyecharts.globals import ThemeType
from sqlalchemy import create_engine
import pandas
from pyecharts import options as opts
from pyecharts.charts import Bar3D, Page, PictorialBar, Pie


def bar_gailan(engine,city,tag):
    def get_data1(tag):
        sql = "select city,avg(avg_wage)as wage from jobs2 where tag like '%{}%' group by city ".format(tag)
        df = pandas.read_sql_query(sql, engine)
        return df

    data = []
    for t in tag:
        df = get_data1(t)
        for x in df.values:
            data.append([t, x[0], x[1]])
    return (
        Bar3D(init_opts=opts.InitOpts(width='1300px', height='600px', theme=ThemeType.VINTAGE))
            .add(
            "",
            data,
            xaxis3d_opts=opts.Axis3DOpts(tag, type_="category", interval=0),
            yaxis3d_opts=opts.Axis3DOpts(city, type_="category", interval=0),
            zaxis3d_opts=opts.Axis3DOpts(type_="value"),
            shading="realistic"
        )
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(max_=200000),
            title_opts=opts.TitleOpts(title="薪资概览"),
        )
            # .render("./result/薪资概览.html")
    )

# def bar_city(engine,city,tag):
#     def get_data2():
#         sql = "select city,avg(max_wage) as max_w,avg(min_wage) as min_w from jobs2 where city is not null group by city"
#         df = pandas.read_sql_query(sql, engine)
#         return df
#
#     d = get_data2()
#     x = list(d.city)
#     y1 = list(d.max_w)
#     y2 = list(d.min_w)
#
#     return (
#         PictorialBar(init_opts=opts.InitOpts(width='400px', height='600px', theme=ThemeType.VINTAGE))
#             .add_xaxis(x)
#             .add_yaxis("最高薪资", y1, label_opts=opts.LabelOpts(is_show=False),
#                        symbol_size=30,
#                        symbol_repeat="fixed",
#                        symbol_offset=[-10, 0],
#                        is_symbol_clip=True,
#                        symbol="image://https://cdn.icon-icons.com/icons2/1675/PNG/128/3890942-bag-cash-currency-euro-money-sack_111189.png",
#                        color="#b7ba6b",
#                        symbol_margin=1)
#             .add_yaxis("最低薪资", y2, label_opts=opts.LabelOpts(is_show=False),
#                        symbol_size=30,
#                        symbol_repeat="fixed",
#                        symbol_offset=[10, 0],
#                        is_symbol_clip=True,
#                        symbol="image://https://cdn.icon-icons.com/icons2/1138/PNG/128/1486395310-14-payment_80577.png",
#                        color="#faa755",
#                        symbol_margin=1)
#             .set_global_opts(title_opts=opts.TitleOpts(title="主要城市薪资分布"))
#             .set_series_opts(
#             label_opts=opts.LabelOpts(is_show=False),
#             markline_opts=opts.MarkLineOpts(
#                 data=[opts.MarkLineItem(y=50, name="yAxis=50")]
#             ),
#         )
#             # .render("./result/主要城市薪资分布.html")
#     )


def bar_tech(engine,city,tag):
    tag = ["前端", "后端", "系统", "安全", "测试", "运维", "数据", "算法"]
    y11 = []
    y22 = []

    def get_data3(tag):
        sql = "select avg(max_wage) as max_w,avg(min_wage) as min_w from jobs2 where tag like '%{}%'".format(tag)
        df = pandas.read_sql_query(sql, engine)
        return df
    for t in tag:
        df = get_data3(t)
        y11.append(df.max_w.values[0])
        y22.append(df.min_w.values[0])
    return (
        PictorialBar(init_opts=opts.InitOpts(width='800px', height='600px', theme=ThemeType.VINTAGE))
            .add_xaxis(tag)
            .add_yaxis("最高薪资", y11, label_opts=opts.LabelOpts(is_show=False),
                       symbol_size=30,
                       symbol_repeat="fixed",
                       symbol_offset=[-10, 0],
                       is_symbol_clip=True,
                       symbol="image://https://cdn.icon-icons.com/icons2/1675/PNG/128/3890942-bag-cash-currency-euro-money-sack_111189.png",
                       color="#b7ba6b",
                       symbol_margin=1)
            .add_yaxis("最低薪资", y22, label_opts=opts.LabelOpts(is_show=False),
                       symbol_size=30,
                       symbol_repeat="fixed",
                       symbol_offset=[10, 0],
                       is_symbol_clip=True,
                       symbol="image://https://cdn.icon-icons.com/icons2/1138/PNG/128/1486395310-14-payment_80577.png",
                       color="#faa755",
                       symbol_margin=1)
            .set_global_opts(title_opts=opts.TitleOpts(title="主要技术薪资分布"))
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(y=50, name="yAxis=50")]
            ),
        )
            # .render("./result/主要技术薪资分布.html")
    )
def pie_xueli(engine,city,tag):
    sql = '''
        select xueli,count(*) as num
        from jobs2
        group by xueli
    '''
    res = pandas.read_sql_query(sql, engine)
    x_data = list(res.xueli)
    y_data = list(res.num)
    data_pair = [list(z) for z in zip(x_data, y_data)]
    data_pair.sort(key=lambda x: x[1])

    return (Pie(init_opts=opts.InitOpts(width='500px', height='600px',theme=ThemeType.VINTAGE))
         .add(
        "",
        data_pair=[list(z) for z in zip(x_data, y_data)],
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
                    "padding": [0, 0],
                    "borderRadius": 0,
                },
            },
        )
    )
         .set_global_opts(
        title_opts=opts.TitleOpts(
            title="学历占比分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23), pos_top='0px', pos_left='180px'),
        tooltip_opts=opts.TooltipOpts(is_show=True),
        legend_opts=opts.LegendOpts(is_show=False)
    )
         # .render("./result/学历占比图.html")
         )


engine = create_engine(
    "mysql+pymysql://{}:{}@{}/{}?charset={}".format('root', 'welcome2019', '127.0.0.1:3306', 'webdataofteachers',
                                                    'utf8mb4'))
def gailan():
    city = [
        "上海",
        "北京",
        "天津",
        "广州",
        "杭州",
        "深圳",
        "苏州",
        "西安",
    ]
    tag = ["前端", "后端", "系统", "安全", "测试", "运维", "数据", "算法"]
    page = Page(layout=Page.SimplePageLayout)
    page.add(bar_gailan(engine,city,tag),pie_xueli(engine,city,tag),bar_tech(engine,city,tag))
    return page