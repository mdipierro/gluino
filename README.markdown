## About gluino

Author: Massimo Di Pierro
License: Web2py license (LGPL) applies to files in minigluon folder

Port of web2py libraries to Bottle, Flask, Pyramid, Tornado with examples.
The port includes;

- Database abstraction layer (dal.py)
- Template language (template.py)
- FORMs (form,py)
- SQLFORMs (sqlhtml.py)
- web2py validators (validators.py)
- web2py cache (cache.py)

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

## Todo

needs more testing