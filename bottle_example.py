from bottle import run, route, request, get, post
from gluino import *
import time

db=DAL('sqlite://storage.sqlite')
db.define_table('person',Field('name',requires=IS_NOT_EMPTY()))

wrapper.debug = True

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

if __name__=='__main__':
    run(host='localhost', poxrt=8080)
