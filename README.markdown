## About gluino

Port of web2py libraries to Bottle, Flask, Pyramid, Tornado, and Wsgiref with examples.

This is a project that started during the PyCon 2012 sprint.

Author: Massimo Di Pierro

License: Web2py license (LGPL) applies to files in gluino/ folder

The port includes;

- Database Abstraction Layer (dal.py) [documentation](http://web2py.com/books/default/chapter/29/6)
- Template language (template.py) [documentation](http://web2py.com/books/default/chapter/29/5)
- FORMs (form,py) [documentation](http://web2py.com/books/default/chapter/29/7#FORM)
- SQLFORMs (sqlhtml.py) [documentation](http://web2py.com/books/default/chapter/29/7#SQLFORM)
- validators (validators.py) [documentation](http://web2py.com/books/default/chapter/29/7#Validators)
- widgets [documentation] (http://web2py.com/books/default/chapter/29/7#Widgets)
- cache (cache.py) [documentation](http://web2py.com/books/default/chapter/29/4#cache)

## Examples

- bottle_example.py
- flask_example.py
- pyramid_example.py
- tornado_example.py
- wsgiref_example.py

pyramid_example.py is also known as [web2pyramid](http://web2pyramid.pylonsproject.org/). It was anticipated long ago but never came to be, until now!

All the examples include the same common code:

    db=DAL('sqlite://storage.sqlite')
    db.define_table('person',Field('name',requires=IS_NOT_EMPTY()))

    ...

    form = SQLFORM(db.person)
    if form.accepts(vars):
        message = 'hello %s' % form.vars.name
    else:
        message = 'hello anonymous'
    people = db(db.person).select()
    now  = cache.ram('time',lambda:time.ctime(),10)
    return locals()

and execute the same template:

    {{extend 'templates/layout.html'}}
    <h1>{{=message}}</h1>
    {{=form}}
    <h2>People</h2>
    {{=people}}
    <h2>Test caching time</h2>
    {{=now}}
    <h2>A static image</h2>
    <img src="/static/cat.jpg" />


which generates the same output on all the frameworks:

![screenshot](https://github.com/mdipierro/gluino/raw/master/static/shot1.png)

## What is missing (compared with web2py)

- sessions (you have to use the session provided by the host framework)
- web2py routing (you have to the routing mechanism of the host framework)
- multi-app support (only web2py does that well)
- the web based IDE (only web2py has it)
- web2py internationalization (you have to use i18n)
- the Role Based Access Control (you have to use the host framework's API)
- web2py's CRON and Scheduler
- form.process() (you have to use form.accepts(...) but works the well)
- everything in contrib (because we did not package it but you can copy it over)
- web2py.js (because we did not package static files here but you can copy it from web2py into static)

## Important

While we guarantee backward compatibility for web2py, we cannot guaranteed backward compatibility for this API since it is very new. Yet the files included here are a subset of web2py/gluon/*.py. We only added the wrapper object (in gluino/__init__.py) and the examples.

## Todo

- more testing
