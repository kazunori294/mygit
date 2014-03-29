# -*- coding:utf-8 -*-

import sys
sys.path.append('libs')

from bottle import route, post, request, redirect, jinja2_template as template

import app.models.manga
model = app.models.manga.Manga()


#一覧ページ
@route('/')
@route('/<page:int>')
def index(page=1):
    result = model.load(page)
    return template('index', result = result)


#新規登録ページ
@route('/new')
def new():
    return template('new')


#編集ページ
@route('/edit/<id:int>')
def edit(id):
    return template('edit', i = model.edit(id))


#DHCP設定ページ
@route('/setdhcp/<id:int>')
def setdhcp(id):
    model.setdhcp(id)
    redirect("/")


#DHCP解除ページ
@route('/deldhcp/<id:int>')
def deldhcp(id):
    model.deldhcp(id)
    redirect("/")

#タスク表示ページ
@route('/task')
def task():
    result = model.task(1)
    return template('task', result = result)


#post送信先
@post('/done')
def done():
    post_data = {}
    post_data["ipaddress"] = request.forms.get('ipaddress')
    post_data["hostname"] = request.forms.get('hostname')
    post_data["macaddress"] = request.forms.get('macaddress')
    post_data["vlan"] = request.forms.get('vlan')
    post_data["purpose"] = request.forms.get('purpose')
    post_data["id"] = request.forms.get('id')
    post_data["del"] = request.forms.get('del')

    model.done(post_data)

    redirect("/")
