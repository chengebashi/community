import pymysql
import numpy
#链接数据库
db = pymysql.connect(host='47.100.253.248', user='community', password='123456', database='community')


def simple_community():
    '''
    展示各种社团基本信息
    :return:
    '''
    db.ping(reconnect=True)
    cur = db.cursor()
    cur.execute("select community_name, community_tips, community_founder, community_createdata, community_hots, id from community_information")
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

def hots():
    '''
    展示社团热度
    :return:
    '''
    db.ping(reconnect=True)
    cur = db.cursor()
    cur.execute("select community_hots from community_information where community_name='网管会'")
    response = cur.fetchall()
    cur.close()
    return response

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

