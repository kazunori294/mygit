# -*- coding: utf-8 -*-

import sys
import bottle
sys.path.append('libs')
bottle.debug(True)

from bottle import route, static_file, default_app
from app.controllers import *


# ==========================================
#   静的なパスを追加
# ==========================================
@route('/stat/<filepath:path>')
def server_static(filepath):
	return static_file(filepath, root='./stat/')

## bottle単品で動かしたい場合
from bottle import run
run(host='0.0.0.0', port=3000,reloader=True)

## gunicornを使う場合
#app = default_app()
