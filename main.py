from flask import Flask, render_template, jsonify, request
import mysql
import numpy

app = Flask(__name__)
# app.secret_key =

@app.route("/")
def index():
    '''主页'''
    response = mysql.simple_community()
    num_len = len(response)
    public = mysql.public_notice()
    return render_template('index.html', response=response, public=public, n=num_len)

@app.route("/base/<id>")
def information(id):
    '''社团详细信息'''
    id = int(id)
    all_information = mysql.community_all(id)[0]
    all_department = mysql.all_department(all_information[1])[0]
    all_department = list(all_department)

    del all_department[0]
    all_department_len = len(all_department)
    for i in range(all_department_len-1, -1, -1):
        if all_department[i] == None:
            all_department.pop(i)
    line_len = len(all_department)
    line_len = int(line_len/2)

    all_dep = numpy.array(all_department).reshape(line_len, 2)
    return render_template('information.html', all_information=all_information, all_department = all_department, all_dep = all_dep)

@app.route("/cname")
def cname():
    '''
    直播界面
    '''
    return render_template('cname.html')

@app.route('/hots')
def hots():
    '''ajax热度点赞'''
    data = request.args.get("hots")
    num = mysql.hots()[0][0]
    reg = {"err":0, "num":num}
    return jsonify(reg)

@app.route('/community_home')
def community_home():
    '''社团大厅'''
    response = mysql.simple_community()
    return render_template('community_home.html', response=response)

@app.route('/tipshome')
def public():
    '''公告大厅'''
    public_tips = mysql.public_notice()
    return render_template('tipshome.html', public_tips=public_tips)




if __name__ == '__main__':
    app.run(debug=True,port=80)