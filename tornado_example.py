import tornado.ioloop
import tornado.web
import time
from gluino import *

db=DAL('sqlite://storage.sqlite')
db.define_table('person',Field('name',requires=IS_NOT_EMPTY()))

wrapper.debug = True
wrapper.http = lambda code, message: tornado.web.HTTPError(code)

class MainHandler(tornado.web.RequestHandler):
    @wrapper(view='templates/index.html',dbs=[db])
    def get(self):
        vars = wrapper.extract_vars(self.request.arguments)
        form = SQLFORM(db.person)
        if form.accepts(vars):
            message = 'hello %s' % form.vars.name
        else:
            message = 'hello anonymous'
        people = db(db.person).select()
        now  = cache.ram('time',lambda:time.ctime(),10)
        return locals()

    def post(self):
        return self.get()

application = tornado.web.Application([
        (r"/index", MainHandler),
        ])

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
