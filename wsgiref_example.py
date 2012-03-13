from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server
from gluino import *
import time
import cgi
import traceback

db=DAL('sqlite://storage.sqlite')
db.define_table('person',Field('name',requires=IS_NOT_EMPTY()))

wrapper.debug = True

@wrapper(view='templates/index.html',dbs=[db])
def index(environ, vars):
    vars = wrapper.extract_vars(vars)
    form = SQLFORM(db.person)
    if form.accepts(vars):
        message = 'hello %s' % form.vars.name
    else:
        message = 'hello anonymous'
    people = db(db.person).select()
    now  = cache.ram('time',lambda:time.ctime(),10)
    return locals()

MAPS = {'/index':index}

# A minimalist example dispatcher
# This is very naive ... bit gives the idea...

def dispatcher(environ, start_response):    
    post = cgi.FieldStorage(
        fp=environ['wsgi.input'],environ=environ,keep_blank_values=True)
    vars = dict((k,post[k].value) for k in post)

    try:
        action = MAPS.get(environ['PATH_INFO'])
        if action:
            body = action(environ, vars)
        else:
            body = 'undefined action: ' + environ['PATH_INFO']
        status = "200 OK"
    except:
        status = "500 INTERNAL ERROR"
        body = traceback.format_exc()
    headers = [('Content-Type', 'text/html'),
               ('Content-Length', str(len(body)))]
    start_response(status,headers)
    return body

if __name__=='__main__':
    httpd = make_server('', 8080, dispatcher)
    print "Serving on port 8080..."
    httpd.serve_forever()
