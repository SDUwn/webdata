import pandas
from pyecharts.charts import PictorialBar, Page, WordCloud, Line, Pie, Geo, Funnel
from pyecharts.globals import ThemeType, ChartType
from pyecharts import options as opts
from sqlalchemy import create_engine


def bar_city(engine,position_type):
    sql = '''
            select city,round(avg(max_wage)) as max_w,round(avg(min_wage)) as min_w
            from jobs2 
            where tag like "%{}%" and city is not null
            group by city
        '''.format(position_type)
    d = pandas.read_sql_query(sql, engine)
    x = list(d.city)
    y1 = list(d.max_w)
    y2 = list(d.min_w)
    return (
        PictorialBar(init_opts=opts.InitOpts(width='650px', height='500px', theme=ThemeType.VINTAGE))
            .add_xaxis(x)
            .add_yaxis("最高薪资", y1,
                       label_opts=opts.LabelOpts(is_show=False),
                       symbol_size=30,
                       symbol_repeat="fixed",
                       symbol_offset=[-10, 0],
                       is_symbol_clip=True,
                       symbol="image://https://cdn.icon-icons.com/icons2/1675/PNG/128/3890942-bag-cash-currency-euro-money-sack_111189.png",
                       color="#b7ba6b",
                       symbol_margin=1)
            .add_yaxis("最低薪资", y2,
                       label_opts=opts.LabelOpts(is_show=False),
                       symbol_size=30,
                       symbol_repeat="fixed",
                       symbol_offset=[10, 0],
                       is_symbol_clip=True,
                       symbol="image://https://cdn.icon-icons.com/icons2/1138/PNG/128/1486395310-14-payment_80577.png",
                       color="#faa755",
                       symbol_margin=1)
            #     .reversal_axis()
            .set_global_opts(title_opts=opts.TitleOpts(title="主要城市薪资分布"))
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(y=50, name="yAxis=50")]
            ),
        )
        # .render("./result/城市薪资分布.html")
    )
def pie_xueli(engine,position_type):
    sql = '''
        select xueli,count(*) as num
        from jobs2
        where tag like "%{}%"
        group by xueli
    '''.format(position_type)
    res = pandas.read_sql_query(sql, engine)
    x_data = list(res.xueli)
    y_data = list(res.num)
    data_pair = [list(z) for z in zip(x_data, y_data)]
    data_pair.sort(key=lambda x: x[1])

    return (Pie(init_opts=opts.InitOpts(width='650px', height='500px',theme=ThemeType.VINTAGE))
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
            title="学历占比分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23), pos_top='0px', pos_left='300px'),
        tooltip_opts=opts.TooltipOpts(is_show=True),
        legend_opts=opts.LegendOpts(is_show=False)
    )
         # .render("./result/学历占比图.html")
         )
def funnel_company(engine,position_type):
    from pyecharts.charts import Funnel
    sql = '''
        select distinct(company),avg_wage/1000 as wage
        from jobs2
        where tag like "%{}%"
        ORDER BY avg_wage DESC
        limit 15
    '''.format(position_type)
    res = pandas.read_sql_query(sql, engine)
    x = list(res.company)
    y = list(res.wage)
    return (
        Funnel(init_opts=opts.InitOpts(width='650px', height='500px',theme=ThemeType.VINTAGE))
            .add(
            series_name="公司-平均薪资(K)",
            data_pair=[list(z) for z in zip(x, y)],
            sort_="ascending",
            label_opts=opts.LabelOpts(position="inside"),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="公司平均薪资漏斗图", title_textstyle_opts=opts.TextStyleOpts(font_size=23),
                                      pos_top='0px', pos_left='250px'),
            legend_opts=opts.LegendOpts(is_show=False))
            # .render("./result/公司平均薪资漏斗图.html")
    )
def wordcloud(engine,position_type):
    import jieba.analyse
    sql = '''
        select detail
        from jobs2
        where tag like '%{}%'
        limit 20
    '''.format(position_type)
    res = pandas.read_sql_query(sql, engine)
    word = []
    count = {}
    for w in res.values:
        word.append(jieba.analyse.extract_tags(w[0], topK=100, withWeight=True))
    for i in word:
        for j in i:
            count[j[0]] = int(j[1] * 1000)
    data = list(count.items())

    return (
        WordCloud(init_opts=opts.InitOpts(width='650px', height='500px',theme=ThemeType.VINTAGE))
            .add(series_name="技术词云分析", data_pair=data, word_size_range=[5, 50], pos_left='150px')
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="技术词云分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23), pos_left='300px'),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
            # .render("./result/词云分析.html")
    )
def zhexian(engine,position_type):
    import pandas
    sql = '''
        select `month`,round(avg(max_wage))as max_wage,round(avg(min_wage)) as min_wage
        from jobs2
        where tag like "%{}%" and `month`!=" "
        group by `month`
    '''.format(position_type)
    res = pandas.read_sql_query(sql, engine)
    x = list(res.month)
    y1 = list(res.max_wage)
    y2 = list(res.min_wage)

    return (
        Line(init_opts=opts.InitOpts(width='650px', height='500px', theme=ThemeType.VINTAGE))
            .add_xaxis(xaxis_data=x)
            .add_yaxis(
            "平均最高薪资",
            y1,
            symbol="image://https://cdn.icon-icons.com/icons2/1675/PNG/128/3890942-bag-cash-currency-euro-money-sack_111189.png",
            symbol_size=20,
            linestyle_opts=opts.LineStyleOpts(color="red", width=3, type_="dashed"),
            itemstyle_opts=opts.ItemStyleOpts(
                border_width=3, border_color="yellow", color="pink"
            ),
        )
            .add_yaxis(
            "平均最低薪资",
            y2,
            symbol="image://https://cdn.icon-icons.com/icons2/1138/PNG/128/1486395310-14-payment_80577.png",
            symbol_size=20,
            linestyle_opts=opts.LineStyleOpts(color="green", width=3, type_="dashed"),
            itemstyle_opts=opts.ItemStyleOpts(
                border_width=3, border_color="yellow", color="blue"
            ),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="薪资变化图"))
            # .render("./result/薪资变化图.html")
    )


def geo(engine,city):
    sql = '''
        select pos,count(*) as c
        from jobs2
        where city="{}" and pos!=" "
        group by pos
    '''.format(city)
    res = pandas.read_sql_query(sql, engine)
    x = list(res.pos)
    y = list(res.c)
    return (
        Geo(init_opts=opts.InitOpts(width='650px', height='600px', theme=ThemeType.VINTAGE))
            .add_schema(maptype=city)
            .add(
            "公司分布",
            [list(z) for z in zip(x, y)],
            type_=ChartType.EFFECT_SCATTER,
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="公司分布"))
        # .render("./result/公司分布.html")
    )
def loudou(engine,city):
    sql = '''
        select company,count(*) as c
        from jobs2
        where city="{}"
        group by company
        order by c DESC
        limit 20
    '''.format(city)
    res = pandas.read_sql_query(sql, engine)
    x = list(res.company)
    y = list(res.c)
    return (
        Funnel(init_opts=opts.InitOpts(width='650px', height='600px', theme=ThemeType.VINTAGE))
            .add(
            "招工数量",
            [list(z) for z in zip(x, y)],
            label_opts=opts.LabelOpts(position="inside"),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="本地名企top20", pos_top='0px', pos_left='250px'),
                             legend_opts=opts.LegendOpts(is_show=False))
            # .render("./result/招工数量top20.html")
    )


engine = create_engine(
    "mysql+pymysql://{}:{}@{}/{}?charset={}".format('root', 'welcome2019', '127.0.0.1:3306', 'webdataofteachers',
                                                    'utf8mb4'))

def part(position_type):
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
    page.add(funnel_company(engine,position_type),zhexian(engine,position_type),wordcloud(engine,position_type),bar_city(engine,position_type))
    return page

def city_part(city):
    page = Page(layout=Page.SimplePageLayout)
    page.add(geo(engine, city), loudou(engine, city))
    return page