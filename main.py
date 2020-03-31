from flask import Flask, render_template, jsonify, request, send_from_directory, session, redirect, abort
import os
import mysql
import numpy
import file_select
import base64

app = Flask(__name__)

#app.secret_key = os.urandom(24)
app.secret_key = b'\xd4\x0e\x15\x15\xc6\xc1P\xc5\xd9!\x8a\xc1\x8fs|xB\x8aA\xd3\x9f#i\xf4'

app.config["UPLOAD_FOLDER"] = r"static\uploads\filedownAndup"
app.config['IMGPATH'] = 'static/uploads/every_life'
app.config['LINSHI'] = 'static/uploads/linshi'
app.config['HEADIMAGE'] = '../static/uploads/community_headimage/'

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@app.route('/login',methods=['POST','GET'])
def login():
    '''登陆 '''
    if request.method == 'POST':
        '''获得前端用户名以及密码，判断是否正确，正确则跳转首页'''
        data = request.get_json()
        user_name = data['userName'].strip()
        pass_word = data['passWord'].strip()
        value = int(data['cars'])
        res = mysql.user_login(user_name,pass_word,value)
        if res == 0:
            session['username'] = user_name
            session['is_super'] = value
            cid = mysql.check_communityid(user_name)
            session['cid'] = cid
            return jsonify({'err': 0})
        elif res ==1:
            return jsonify({'err':'密码错误或身份不正确！！'})
        elif res == 2:
            return jsonify({'err':'用户不存在'})
    else:
        login = session.get("username")
        if login:
            rsp = '/'
            return redirect(rsp)
        else:
            return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username')
    session.pop('is_super')
    session.pop('cid')
    return redirect('/')
# @app.route('/register',methods=['GET','POST'])
# def register():
#     '''注册'''
#     if request.method == 'GET':
#         login = session.get("username")
#         value = session.get('is_super')
#         if login:
#             if value == 0:
#                 rsp = '/'
#                 return redirect(rsp)
#             else:
#                 abort(404)
#
#         else:
#             return render_template('index.html')
#
#     else:
#         data = request.get_json()   #获取前端ajax传递的post参数转化为了字典
#         user_name = data['name']
#         pass_word = data['passWord']
#         value = int(data['value'])
#         print(user_name, pass_word, value)
#         return jsonify({'err':1})

@app.route('/send_info')
def send_info():
    '''用户注册社团'''
    user_name = session.get('username')
    value = session.get('is_super')
    cid = session.get('cid')
    return render_template('send_info.html',uname = user_name,is_super = value,cid = cid)

@app.route("/")
def index():
    '''主页'''
    user_name = session.get('username')
    value = ''
    if user_name == None:
        user_name = ''
    else:
        value = session.get('is_super')
    response = mysql.simple_community()
    num_len = len(response)
    public = mysql.public_notice()
    file_list = file_select.filesshow()
    file_list = file_list[0:3]
    cid = session.get('cid')
    return render_template('index.html', response=response, public=public, n=num_len, file_list=file_list,uname = user_name,is_super = value,cid=cid)

@app.route("/base/<id>")
def information(id):
    '''社团详细信息'''
    id = int(id)
    all_information = mysql.community_all(id)[0]
    all_department = mysql.all_department(all_information[1])
    all_department = list(all_department)    #数据库取出的数据元组列表化
    # print(all_department)
    if  not all_department:
        all_department = ['空','空']
    else:
        all_department = list(all_department[0])
        del all_department[0]                              #删除列表首个元素
        all_department_len = len(all_department)           #列表长度
        for i in range(all_department_len-1, -1, -1):      #循环去除列表中None
            if all_department[i] == None:
                all_department.pop(i)
    line_len = len(all_department)       #重新计算列表长度
    line_len = int(line_len/2)        #定义二维列表的行数
    all_dep = numpy.array(all_department).reshape(line_len, 2)      #生成一个三行二列的二维列表
    community_name = all_information[1]  #取社团名
    founder = all_information[3]
    hots = all_information[-2]

    images_path_rel = os.path.join(app.config['IMGPATH'],community_name)
    if not os.path.exists(images_path_rel):
        os.mkdir(images_path_rel)
    list_root = os.listdir(images_path_rel)    #遍历出所有图片
    images_list = [os.path.join(community_name,i) for i in list_root] #形成图片路径

    images_path_rel_2 = os.path.join(app.config['LINSHI'], community_name)
    if not os.path.exists(images_path_rel_2):
        os.mkdir(images_path_rel_2)
    list_root_2 = os.listdir(images_path_rel_2)  # 遍历出所有图片
    images_list_2 = [os.path.join(community_name, i) for i in list_root_2]  # 形成图片路径
    user_name = session.get('username')
    value = session.get('is_super')
    cid = session.get('cid')
    return render_template('information.html', all_information=all_information, all_department = all_department, all_dep = all_dep, images_life = images_list[:6],login_name=login, images_file_2=images_list_2[:6],uname = user_name,is_super = value,founder=founder, hots=hots ,cid=cid)


@app.route('/hots',methods=['GET','POST'])
def hots():
    '''ajax热度点赞'''
    if request.method == 'POST':
        data = request.get_json()
        founder = data['founder'].strip()
        # print(founder,'founder')
        chots = mysql.hots_add(founder)
        if chots == -1:
            reg = {'err':'后台错误'}
        else:
            reg = {"err":0, "num":chots}
        return jsonify(reg)

@app.route('/community_home')
def community_home():
    '''社团大厅'''
    user_name = session.get('username')
    value = session.get('is_super')
    cid = session.get('cid')
    response = mysql.simple_community()
    return render_template('community_home.html', response=response,uname = user_name,is_super = value,cid=cid)

@app.route('/tipshome')
def public():
    '''公告大厅'''
    user_name = session.get('username')
    value = session.get('is_super')
    cid = session.get('cid')
    public_tips = mysql.public_notice()
    public_tips = list(public_tips)[::-1]
    return render_template('tipshome.html', public_tips=public_tips,uname = user_name,is_super = value,cid=cid)

@app.route('/myinfo',methods=['GET','POST'])
def myinfo():
    '''个人信息'''
    if request.method == 'GET':
        user_name = session.get('username')
        community_name = mysql.check_community(user_name)
        value = session.get('is_super')
        cid = session.get('cid')
        return render_template('myinfo.html',uname=user_name, is_super = value, cname = community_name,cid=cid)
    else:
        data = request.get_json()
        uname = data['uname'].strip()
        shetuan_name = data['shetuan'].strip()
        haibao = data['haibao'].strip()
        haibao = os.path.basename(haibao)
        shuliang = int(data['shuliang'])
        shijian = data['shijian'].strip()
        jianjie = data['jianjie'].strip()
        chengjiu = data['chengjiu'].strip()
        haibao_img = data['haibao_img']
        path = os.path.join(app.config['HEADIMAGE'][3:], shetuan_name)
        if not os.path.exists(path):
            os.mkdir(path)
        haibao_path = os.path.join(path,haibao)
        with open(haibao_path,'wb') as f:
            img = base64.b64decode(haibao_img.split(',')[-1])
            f.write(img)
        # new_haibao = '../'+haibao_path
        # print(new_haibao,'123')
        haibao_path = '../' + path + '/' + haibao
        res = mysql.update_community(uname,haibao_path,shuliang,shijian,jianjie,chengjiu)
        if res == 1:
            return jsonify({'err':'后台错误'})
        else:
            return jsonify({'err':0})


@app.route('/data_home')
def data_home():
    '''资料大厅'''
    user_name = session.get('username')
    value = session.get('is_super')
    file_list = file_select.filesshow()
    cid = session.get('cid')
    return render_template("data_home.html",file_list=file_list,uname = user_name,is_super = value,cid=cid)

@app.route('/regist_user')
def regist_user():
    '''注册新的社团用户'''
    user_name = session.get('username')
    value = session.get('is_super')
    cid = session.get('cid')
    return render_template('regist_user.html',uname = user_name,is_super = value,cid=cid)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['chenge']
        file_name = file.filename
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
        file.save(file_path)
        reg = {'err':0}
    except:
        reg = {'err':1}
    return jsonify(reg)

@app.route('/indexdonw/<filename>')
def index_down(filename):
    return send_from_directory(os.path.join(app.config["UPLOAD_FOLDER"]), filename)

@app.route('/downhome/<filename>')
def file_down(filename):
    return send_from_directory(os.path.join(app.config["UPLOAD_FOLDER"]),filename)


@app.route('/addimages',methods=['GET','POST'])
def addimage():
    '''接收发过来的社团生活照'''
    if request.method == 'POST':
        data = request.get_json()
        img_path = os.path.join(app.config['IMGPATH'],data['community'][6:])
        if not os.path.exists(img_path):
            os.mkdir(img_path)
        image_name = [i['name'] for i in data['image_data']]
        image_content = [i['base64'].split(',')[-1] for i in data['image_data']]
        image_dict = [{'name':image_name[i], 'content':image_content[i]} for i in range(len(image_name))]
        for i in image_dict:
            with open(os.path.join(img_path,i['name']),'wb') as f:
                data_img = base64.b64decode(i['content'])
                f.write(data_img)
        reg = {'err': 0}
        return jsonify(reg)


@app.route('/linshi_photo',methods=['GET','POST'])
def linshi_photo():
    '''上传拍照图片'''
    if request.method == 'POST':
        data = request.get_json()
        community_name = data['community'][6:]
        path = os.path.join(app.config['LINSHI'],community_name)
        data_img = data['image']
        if not os.path.exists(path):
            os.mkdir(path)
        image_content = [i.split(',')[-1] for i in data_img]
        print(image_content)
        for i in image_content:
            with open(os.path.join(path,mysql.random_number()),'wb') as f:
                data_img = base64.b64decode(i)
                f.write(data_img)
        reg = {'err': 0}
        return jsonify(reg)

@app.route('/sendallinfo',methods=['GET','POST'])
def sendallinfo():
    '''拿到数据注册用户以及社团并发邮件给超管'''
    if request.method == 'POST':
        data = request.get_json()
        community_name = data['com_name']
        user_name = data['usr_name']
        password = data['password']
        email_value = data['email_value']
        community_name = '社团名:' + community_name +'\n'
        user_name = '用户名：' + user_name + '\n'
        password = '密码：' + password + '\n'
        user_email = '邮箱：' + email_value + '\n'
        text_mail = community_name + user_name + password + user_email
        res = mysql.email_send(text_mail,'新社团注册','1624324870@qq.com')
        if res == 0:
            return jsonify({'err':0})
        else:
            return jsonify({'err':'注册失败请联系管理员'})

@app.route('/register_newuser',methods=['GET','POST'])
def register_newuser():
    '''注册新用户以及社团'''
    if request.method == 'POST':
        data = request.get_json()
        username = data['uname']
        password = data['pwd']
        cname = data['cname']
        email = data['email']
        rer = mysql.register_community(cname,username)
        if rer == 1:
            print(1)
            return jsonify({'err':'注册社团失败'})
        else:
            ree = mysql.register_communityuser(username, password, email)
            if ree == 1:
                return jsonify({'err':'用户名存在'})
            elif ree == 2:
                return jsonify({"err":'系统未知错误'})
            else:
                reg = mysql.email_send('注册成功，邮件已发至用户邮箱，请尽快添加社团信息！','审核通过',email)
                if reg==0:
                    return jsonify({"err": 0})
                else:
                    return jsonify({"err":'网络错误!'})


@app.route('/updateinfo',methods=['GET','POST'])
def updateinfo():
    '''修改部门信息'''
    if request.method == 'POST':
        data = request.get_json()
        cname = data['cname'].strip()
        depart = data['department']
        res = mysql.update_departe(cname,depart)
        if res == 1:
            return jsonify({'err':'后台错误'})
        else:
            return jsonify({'err':0})
    else:
        user_name = session.get('username')
        community_name = mysql.check_community(user_name)
        value = session.get('is_super')
        cid = session.get('cid')
        return render_template('myinfo_depart.html', uname=user_name, is_super=value, cname=community_name,cid=cid)


@app.route('/userlist',methods=['GET','POST'])
def userlist():
    '''展示用户用户名以及密码'''
    user_list = mysql.show_user()
    user_name = session.get('username')
    value = session.get('is_super')
    cid = session.get('cid')
    return render_template('userlist.html',userlist=user_list,uname = user_name,is_super = value,cid=cid)

@app.route('/search',methods=['GET','POST'])
def search():
    '''展示搜索结果'''
    if request.method=='POST':
        search_name = request.form.get('s')
        resg = mysql.search_response(search_name)
        return render_template('community_search.html', resg = resg)

@app.route('/send_public',methods=['GET','POST'])
def send_public():
    '''发布公告'''
    if request.method=='POST':
        data = request.get_json()
        cname = data['cname'].strip()
        gonggao = data['gonggao'].strip()
        res = mysql.add_public(cname,gonggao)
        if res == 1:
            return jsonify({'err':'数据库出错'})
        else:
            return jsonify({'err':0})
    else:
        user_name = session.get('username')
        value = session.get('is_super')
        cid = session.get('cid')
        cname = mysql.check_community(user_name)
        return render_template('send_public.html',uname = user_name,is_super = value,cid=cid,cname=cname)

if __name__ == '__main__':
    app.run(debug=True,port=8000)