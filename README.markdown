## About gluino

Author: Massimo Di Pierro
License: Web2py license (LGPL) applies to files in minigluon folder

Port of web2py libraries to Bottle, Flask, Pyramid, Tornado with examples.
The port includes;

- Database Abstraction Layer (dal.py) [documentation](http://web2py.com/books/default/chapter/29/6)
- Template language (template.py) [documentation](http://web2py.com/books/default/chapter/29/5)
- FORMs (form,py) [documentation](http://web2py.com/books/default/chapter/29/7#FORM)
- SQLFORMs (sqlhtml.py) [documentation](http://web2py.com/books/default/chapter/29/7#SQLFORM)
- web2py validators (validators.py) [documentation](http://web2py.com/books/default/chapter/29/7#Validators)
- web2py widgets [documentation] (http://web2py.com/books/default/chapter/29/7#Widgets)
- web2py cache (cache.py) [documentation](http://web2py.com/books/default/chapter/29/4#cache)

## Examples

- bottle_example.py
- flask_example.py
- pyramid_example.py
- tornado_example.py
- wsgiref_example.py

All the examples include the same common code:

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

- sessions (you have to use the session provided by your framework)
- multi-app support
- the web based IDE
- web2py internationalization (you have to use i18n)
- the Role Based Access Control (you have to use your framework's API)
- web2py's CRON and Scheduler
- form.process() (you have to use form.accepts(...))
- everything in contrib (because we did not package it but you can copy it over)
- web2py.js (again because we did not package but you can copy it over)

## Todo

- more testing
