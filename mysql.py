import pymysql

#链接数据库
db = pymysql.connect(host='47.100.253.248', user='community', password='123456', database='community')


def simple_community():
    '''
    展示各种社团基本信息
    :return:
    '''
    db.ping(reconnect=True)
    cur = db.cursor()
    cur.execute("select community_name, community_tips, community_founder, community_createdata, community_hots from community_information")
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

