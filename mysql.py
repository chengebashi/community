import pymysql
import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header
#链接数据库
db = pymysql.connect(host='127.0.0.1', user='community', password='123456', database='community')


def random_number():
    num = random.randint(100000,999999)
    num_name = str(num)+'.png'
    return num_name

def simple_community():
    '''
    展示各种社团基本信息
    :return:
    '''
    db.ping(reconnect=True)
    cur = db.cursor()
    cur.execute("select community_name, community_tips, community_founder, community_createdata, community_hots, id, community_headimage from community_information")
    response = cur.fetchall()
    cur.close()
    return response

def public_notice():
    '''
    展示公告信息
    :return:
    '''
    db.ping(reconnect=True)
    cur = db.cursor()
    cur.execute("select community_name, community_public_notice, community_time from community_public")
    response = cur.fetchall()
    cur.close()
    return response

def hots(founder):
    '''
    展示社团热度
    :return:
    '''
    db.ping(reconnect=True)
    cur = db.cursor()
    cur.execute("select community_hots from community_information where community_founder='{}'".format(founder))
    response = cur.fetchall()
    cur.close()
    return response[0][0]

def hots_add(founder):
    '''增加点赞'''
    db.ping(reconnect=True)
    try:
        cur = db.cursor()
        res = hots(founder)
        res = int(res)+1
        cur.execute("update community_information set community_hots={} where community_founder='{}'".format(res,founder))
        db.commit()
        res_2 = hots(founder)
        cur.close()
        return res_2
    except:
        return -1

def community_all(id):
    '''
    根据id来查找社团的所有信息
    :return:
    '''
    db.ping(reconnect=True)
    cur = db.cursor()
    cur.execute("select * from community_information where id={}".format(id))
    response = cur.fetchall()
    cur.close()
    return response

def all_department(community_name):
    '''
    根据社团名查找部门信息
    :param community_name:
    :return:
    '''
    db.ping(reconnect=True)
    cur = db.cursor()
    cur.execute("select * from community_department where community_name='{}'".format(community_name))
    response = cur.fetchall()
    cur.close()
    return response

def user_login(username,password,value):
    '''
    验证用户名以及密码是否正确
    :param username:
    :param password:
    :param value:
    :return: 0代表验证无误 1代表密码错误 2代表用户名不存在
    '''
    db.ping(reconnect=True)
    cur = db.cursor()
    cur.execute("select * from community_user where community_username = '{}'".format(username))
    response = cur.fetchall()
    if not response:
        return 2
    else:
        cur.execute("select community_password from community_user where community_username = '{}'and community_type = '{}'".format(username,value))
        response = cur.fetchall()
        if response:
            return 0
        else:
            return 1



def register_community(community_name,username):
    '''
    注册新社团
    :return:
    '''
    try:
        db.ping(reconnect=True)
        cur = db.cursor()
        cur.execute("INSERT INTO community_information values (DEFAULT, '{}', DEFAULT, '{}', DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT)".format(community_name,username))
        db.commit()
        return 0
    except:
        return 1


def register_communityuser(uname,pword,email):
    '''
    注册新用户
    :return: 0表示成功，1表示用户名已存在,2表示未知错误
    '''
    db.ping(reconnect=True)
    cur = db.cursor()
    try:
        cur.execute("SELECT * from community_user WHERE community_username='{}'".format(uname))
        response = cur.fetchall()
        if response:
            return 1
        else:
            cur.execute("INSERT INTO community_user values (DEFAULT, '{}', '{}', '{}','1')".format(uname,pword,email))
            db.commit()
            return 0
    except:
        return 2

def email_send(text, title, email):
    '''
    发邮件
    :return:
    '''
    # 第三方 SMTP 服务
    mail_host = "smtp.exmail.qq.com"  # 设置服务器
    mail_user = "chenge@chenge.online"  # 用户名
    mail_pass = "QrwdCHPzdZPga835"  # 口令

    sender = 'chenge@chenge.online'
    receivers = [email]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(text, 'plain', 'utf-8')
    message['From'] = Header("chenge", 'utf-8')
    message['To'] = Header("myself", 'utf-8')

    subject = title
    message['Subject'] = Header(subject, 'utf-8')

    try:
        print(1)
        smtpObj = smtplib.SMTP_SSL(host='smtp.exmail.qq.com')
        print(2)
        smtpObj.connect(mail_host, 465)  # 25 为 SMTP 端口号
        # smtplib.SMTP_SSL(host='smtp.gmail.com').connect(host='smtp.gmail.com', port=465)
        print(3)
        smtpObj.login(mail_user, mail_pass)
        print(4)
        smtpObj.sendmail(sender, receivers, message.as_string())
        return 0
    except smtplib.SMTPException:
        return 1

def check_community(user_name):
    '''校验社团'''
    db.ping(reconnect=True)
    cur = db.cursor()
    cur.execute("select community_name from community_information where community_founder='{}'".format(user_name))
    response = cur.fetchall()
    cur.close()
    return response[0][0]

def check_communityid(user_name):
    '''校验社团'''
    db.ping(reconnect=True)
    cur = db.cursor()
    cur.execute("select id from community_information where community_founder='{}'".format(user_name))
    response = cur.fetchall()
    print(response)
    cur.close()
    return response[0][0]


def update_community(uname,haibao,shuliang,shijian,jianjie,chengjiu):
    '''修改社团信息'''
    db.ping(reconnect=True)
    try:
        cur = db.cursor()
        print(haibao,'321')
        cur.execute("update community_information set community_headimage = '{}',community_people= {},community_createdata='{}',community_tips='{}',community_success='{}' where community_founder='{}'".format(haibao,shuliang,shijian,jianjie,chengjiu,uname))
        db.commit()
        cur.close()
        return 0
    except Exception as f:
        print(f)
        return 1

def update_departe(cname, department):
    '''修改部门信息'''
    db.ping(reconnect=True)
    department_len = len(department)
    try:
        cur = db.cursor()
        cur.execute("select * from community_department where community_name='{}'".format(cname))
        response = cur.fetchall()
        if not response:
            cur.execute("INSERT INTO community_department values ('{}', DEFAULT, DEFAULT, DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)".format(cname))
            db.commit()
        else:
            if department_len == 1:
                cur.execute("update community_department set department_first = '{}',department_first_note= '{}' where community_name ='{}'".format(department[0][0],department[0][1],cname))
            elif department_len == 2:
                cur.execute(
                    "update community_department set department_first = '{}',department_first_note= '{}',department_second='{}',department_second_note='{}' where community_name ='{}'".format(
                        department[0][0], department[0][1], department[1][0],department[1][1],cname))
            elif department_len == 3:
                cur.execute(
                    "update community_department set department_first = '{}',department_first_note= '{}',department_second='{}',department_second_note='{}',department_third='{}',department_third_note='{}' where community_name ='{}'".format(
                        department[0][0], department[0][1], department[1][0], department[1][1], department[2][0], department[2][1], cname))
            elif department_len == 4:
                cur.execute(
                    "update community_department set department_first = '{}',department_first_note= '{}',department_second='{}',department_second_note='{}',department_third='{}',department_third_note='{}',department_fourth='{}',department_fourth_note='{}' where community_name ='{}'".format(
                        department[0][0], department[0][1], department[1][0], department[1][1], department[2][0],department[2][1],department[3][0],department[3][1], cname))
            elif department_len == 5:
                cur.execute(
                    "update community_department set department_first = '{}',department_first_note= '{}',department_second='{}',department_second_note='{}',department_third='{}',department_third_note='{}',department_fourth='{}',department_fourth_note='{}',department_fifth='{}',department_fifth_note='{}' where community_name ='{}'".format(
                        department[0][0], department[0][1], department[1][0], department[1][1], department[2][0],
                        department[2][1], department[3][0], department[3][1], department[4][0], department[4][1], cname))
            db.commit()
            cur.close()
        return 0
    except Exception as f:
        print(f)
        return 1

def show_user():
    '''展示用户名'''
    db.ping(reconnect=True)
    cur = db.cursor()
    cur.execute("select community_username,community_password,community_email from community_user")
    response = cur.fetchall()
    cur.close()
    return list(response)

def search_response(search_name):
    '''返回所有模糊搜索的社团'''
    search_all = []
    db.ping(reconnect=True)
    cur = db.cursor()
    cur.execute("select community_name from community_information where community_name regexp '[{}]'".format(search_name))
    response = cur.fetchall()
    search_list = [i[0] for i in response]
    for j in search_list:
        cur.execute("select  community_name, community_tips, community_founder, community_createdata, community_hots, id from community_information where community_name = '{}'".format(j))
        res = cur.fetchall()
        search_all.append(list(res[0]))
    cur.close()
    print(search_all)
    return search_all


def add_public(cname,gonggao):
    '增加公告'
    db.ping(reconnect=True)
    try:
        cur = db.cursor()
        cur.execute("insert INTO community_public values ('{}','{}', now())".format(cname,gonggao))
        db.commit()
        cur.close()
        return 0
    except:
        return 1