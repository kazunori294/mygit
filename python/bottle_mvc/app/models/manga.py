# -*- coding:utf-8 -*-

import app.models.db as db
import app.models.pager as pager

class Manga:


    # ==========================================
    #
    # タスク一覧を取得するやーつ
    #
    # ==========================================

    def task(self, page):

        define_page = 100
        start = (page - 1) * define_page

        result = {}

        sql = "select count(task_id) as all_count from task"
        db.con.execute(sql)
        result = db.con.fetchone()

        result["pagination"] = pager.Pagination(page, define_page, result["all_count"])

        sql = "select * from task order by task_id DESC"
        sql += ' limit %s, %s'
        db.con.execute(sql, (start, define_page))
        result["tasklist"] = db.con.fetchall()

        return result


    # ==========================================
    # 
    # マンガ一覧を取得するやーつ
    # 
    # ==========================================

    def load(self, page):

        define_page = 100
        start = (page - 1) * define_page

        result = {}

        sql = "select count(id) as all_count from iplist"
        db.con.execute(sql)
        result = db.con.fetchone()

        result["pagination"] = pager.Pagination(page, define_page, result["all_count"])

        sql = "select * from iplist order by ipaddress"
        sql += ' limit %s, %s'
        db.con.execute(sql, (start, define_page))
        result["iplists"] = db.con.fetchall()

        return result


    # ==========================================
    # 
    # マンガ単品を取得するやーつ
    # 
    # ==========================================
    def edit(self, id):

        sql = "select * from iplist where id = %s"
        db.con.execute(sql, (id))
        return db.con.fetchone()


    # ==========================================
    # 
    # idがあったらdelフラグありで削除、無しで更新、idがなかったら新規追加
    # ==========================================
    def done(self, params):

        if params["id"]:

            if params["del"]:
                sql = "delete from iplist where id = %s"
                db.con.execute(sql, (params["id"]))

            else:
                sql = "update iplist set "
                sql += " ipaddress=%s"
                sql += ",hostname=%s"
                sql += ",macaddress=%s"
                sql += ",vlan=%s"
                sql += ",purpose=%s"
                sql += ",regdate=CURRENT_TIMESTAMP"
                sql += " where id = %s"
                db.con.execute(sql, (
                              		params["ipaddress"],
                                	params["hostname"],
                                	params["macaddress"],
                                	params["vlan"],
                                	params["purpose"],
                                	params["id"]
                                    ))

        else:

            sql = "insert into iplist (ipaddress, hostname, macaddress, vlan, purpose, regdate) values (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)"
            db.con.execute(sql, (
                                params["ipaddress"],
                                params["hostname"],
                                params["macaddress"],
                                params["vlan"],
                                params["purpose"]
				 ))

        db.dbhandle.commit()
        return


    # ==========================================
    #
    # DHCP設定を行うやーつ
    # 　-dhcpカラムをsetにする
    # 　-dhcpd.confに追加する
    # ==========================================
    def setdhcp(self, id):

        sql = "update iplist set dhcp='set' where id = %s"
        db.con.execute(sql, (id))
        db.dbhandle.commit()

	sql = "select * from iplist where id = %s"
	db.con.execute(sql,(id))
	result = db.con.fetchone()

	hostname = str(result["hostname"])
	macaddress = str(result["macaddress"])
	ipaddress = str(result["ipaddress"])

	fp = open('/dhcp/dhcpd-reservations.conf', 'a')
	fp.write('host ' + hostname + ' { hardware ethernet ' + macaddress + '; fixed-address ' + ipaddress + ';}\n')
	fp.close()
	
        return



    # ==========================================
    #
    # DHCP設定を解除するやーつ
    # 　-dhcpカラムをunsetにする
    # 　-dhcpd.confに追加する
    # ==========================================
    def deldhcp(self, id):

        sql = "update iplist set dhcp='unset' where id = %s"
        db.con.execute(sql, (id))
        db.dbhandle.commit()

        sql = "select * from iplist where id = %s"
        db.con.execute(sql,(id))
        result = db.con.fetchone()
 
        f = open('/dhcp/dhcpd-reservations.conf')
        lines = f.readlines()
        f.close()

        fp = open('/dhcp/dhcpd-reservations.conf', 'w')
        
        ipaddress = str(result["ipaddress"])       
        for line in lines:
          if not ipaddress in line:
            fp.write(line)

        fp.close()

        return


    # ==========================================
    #
    # VM一覧を取得するやーつ
    #
    # ==========================================

    def atask(self, page):

        define_page = 100
        start = (page - 1) * define_page

        result = {}

        sql = "select count(task_id) as all_count from task"
        db.con.execute(sql)
        result = db.con.fetchone()

        result["pagination"] = pager.Pagination(page, define_page, result["all_count"])

        sql = "select * from task order by task_id DESC"
        sql += ' limit %s, %s'
        db.con.execute(sql, (start, define_page))
        result["tasklist"] = db.con.fetchall()

        return result

