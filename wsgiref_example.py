from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server
from gluino import wrapper, DAL, Field, SQLFORM, cache, IS_NOT_EMPTY
import time
import cgi
import traceback

# configure the gluino wrapper
wrapper.debug = True

# create database and table
db=DAL('sqlite://storage.sqlite')
db.define_table('person',Field('name',requires=IS_NOT_EMPTY()))

# define action
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

# A minimalist example dispatcher
# This is very naive ... bit gives the idea...
 
MAPS = {'/index':index}

def dispatcher(environ, start_response):    
    post = cgi.FieldStorage(
        fp=environ['wsgi.input'],environ=environ,keep_blank_values=True)
    vars = dict((k,post[k].value) for k in post)

    try:
        uri = environ['PATH_INFO']
        if uri.startswith('/static/'):
            body = open(uri[1:],'rb').read()
        else:
            action = MAPS.get(uri)
            if action:
                body = action(environ, vars)
            else:
                body = 'undefined action: ' + uri
        status = "200 OK"
    except:
        status = "500 INTERNAL ERROR"
        body = traceback.format_exc()
    headers = [('Content-Type', 'text/html'),
               ('Content-Length', str(len(body)))]
    start_response(status,headers)
    return body

# start the web server
if __name__=='__main__':
    httpd = make_server('', 8080, dispatcher)
    print "Serving on port 8080..."
    httpd.serve_forever()
