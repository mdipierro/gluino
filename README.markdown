Author: Massimo Di Pierro
License: Web2py license (LGPL) applies to files in minigluon folder

Port of web2py to Bottle, Flask and Pyramid with examples.
The port includes;

- web2py Database abstraction layer
- web2py Template language
- web2py FORMs
- web2py SQLFORMs
- web2py validators

This is a work in progress and needs testing:

- bottle_example.py
- flask_example.py
- pyramid_example.py
- tornado_example.py

## API

The @wrapper decorator is very important. It needs to know the view/template filename (index.html in the example), a list of databases to be wrapped in a transaction.

## TODO

- support upload type fields
- The web2py objects: session, redirect, HTTP and URL are not supported and will cause when called internally.
