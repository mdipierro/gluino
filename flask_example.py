from flask import Flask, request, session, redirect
from gluino import wrapper, DAL, Field, SQLFORM, cache, IS_NOT_EMPTY
import time

# configure the gluino wrapper                                      
wrapper.debug = True
wrapper.redirect = lambda status, url: redirect(url)

# initialize flask
app = Flask(__name__)
app.config.from_object(__name__)

# create database and table
db=DAL('sqlite://storage.sqlite')
db.define_table('person',Field('name',requires=IS_NOT_EMPTY()))

# define action
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

# start web server
if __name__=='__main__':
    print 'serving from port 8080...'
    app.run(port=8080)
