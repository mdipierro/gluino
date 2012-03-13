from flask import Flask, request, session, redirect
from gluino import *
import time

app = Flask(__name__)
app.config.from_object(__name__)

db=DAL('sqlite://storage.sqlite')
db.define_table('person',Field('name',requires=IS_NOT_EMPTY()))

wrapper.debug = True

@app.route('/index',methods=['GET','POST'])
@wrapper(view='templates/index.html',dbs=[db])
def index():
    vars = wrapper.extract_vars(request.form)
    form = SQLFORM(db.person)
    if form.accepts(vars):
        message = 'hello %s' % form.vars.name
    else:
        message = 'hello anonymous'
    people = db(db.person).select()
    now  = cache.ram('time',lambda:time.ctime(),10)
    return locals()

if __name__=='__main__':
    app.run(port=8080)
