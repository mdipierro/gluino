from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.static import static_view
from pyramid.httpexceptions import HTTPFound
from gluino import wrapper, DAL, Field, SQLFORM, cache, IS_NOT_EMPTY
import time

# configure the gluino wrapper
wrapper.debug = True
wrapper.response = Response
wrapper.redirect = lambda status,url: HTTPFound(location=url)

# create database and table
db=DAL('sqlite://storage.sqlite')
db.define_table('person',Field('name',requires=IS_NOT_EMPTY()))

# define action
@wrapper(view='templates/index.html',dbs=[db])
def index(context, request):
    vars = wrapper.extract_vars(request.POST)
    form = SQLFORM(db.person)
    if form.accepts(vars):
        message = 'hello %s' % form.vars.name
    else:
        message = 'hello anonymous'
    people = db(db.person).select()
    now  = cache.ram('time',lambda:time.ctime(),10)
    return locals()

# start web server
if __name__=='__main__':
    config = Configurator()
    config.add_route('index', '/index')
    config.add_view(index, route_name='index')
    config.add_static_view(name='static', path='static')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()

