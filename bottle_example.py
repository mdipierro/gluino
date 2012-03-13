from bottle import run, route, request, get, post, static_file, redirect
from gluino import *
import time

# configure the gluino wrapper
wrapper.debug = True
wrapper.redirect = lambda status,url: redirect(url)

# create database and table
db=DAL('sqlite://storage.sqlite')
db.define_table('person',Field('name',requires=IS_NOT_EMPTY()))

# define action
@get('/index')
@post('/index')
@wrapper(view='templates/index.html',dbs=[db])
def index():
    vars = wrapper.extract_vars(request.forms)
    form = SQLFORM(db.person)
    if form.accepts(vars):
        message = 'hello %s' % form.vars.name
    else:
        message = 'hello anonymous'
    people = db(db.person).select()
    now  = cache.ram('time',lambda:time.ctime(),10)
    return locals()

# handle static files
@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='static')

#start web server
if __name__=='__main__':
    run(host='localhost', port=8080)
