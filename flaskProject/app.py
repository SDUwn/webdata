from flask import Flask,render_template
from pythonfile.graph import zju_page,hust_page,ict_page,ia_page,shanghaitech_page,fudan_page
from markupsafe import Markup
from pythonfile.work_graph import gailan
from pythonfile.work_part import part, city_part

app = Flask(__name__)


@app.route('/')
def test():
    return render_template("test.html")

@app.route('/graph')
def world_cloud_graph():
    # return render_template('zju.html')
    return Markup(zju_page().render_embed())

@app.route('/hust')
def hust_graph():
    return Markup(hust_page().render_embed())

@app.route('/ict')
def ict_graph():
    return Markup(ict_page().render_embed())

@app.route('/ia')
def ia_graph():
    return Markup(ia_page().render_embed())

@app.route('/shanghaitech')
def shanghaitech_graph():
    return Markup(shanghaitech_page().render_embed())

@app.route('/fudan')
def fudan_graph():
    return Markup(fudan_page().render_embed())

@app.route('/work/')
def work():
    return render_template('work.html')

@app.route('/all/')
def all_():
    return Markup(gailan().render_embed())
@app.route('/qianduan/')
def qian():
    return Markup(part("前端").render_embed())
@app.route('/houduan/')
def hou():
    return Markup(part("后端").render_embed())
@app.route('/yunwei/')
def yun():
    return Markup(part("运维").render_embed())
@app.route('/ceshi/')
def ce():
    return Markup(part("测试").render_embed())
@app.route('/shuju/')
def shu():
    return Markup(part("数据").render_embed())
@app.route('/suanfa/')
def suan():
    return Markup(part("算法").render_embed())
@app.route('/xitong/')
def xi():
    return Markup(part("系统").render_embed())
@app.route('/anquan/')
def an():
    return Markup(part("安全").render_embed())

@app.route('/beijing/')
def bei():
    return Markup(city_part("北京").render_embed())
@app.route('/shanghai/')
def shang():
    return Markup(city_part("上海").render_embed())
@app.route('/guangzhou/')
def guang():
    return Markup(city_part("广州").render_embed())
@app.route('/shenzhen/')
def shen():
    return Markup(city_part("深圳").render_embed())
@app.route('/hangzhou/')
def hang():
    return Markup(city_part("杭州").render_embed())
@app.route('/suzhou/')
def su():
    return Markup(city_part("苏州").render_embed())
@app.route('/tianjin/')
def tian():
    return Markup(city_part("天津").render_embed())
@app.route('/xian/')
def xi_():
    return Markup(city_part("西安").render_embed())

if __name__ == '__main__':
    app.run(debug=True)
