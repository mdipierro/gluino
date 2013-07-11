# Name: gluino
# Author: Massimo Di Pierro
# License: LGPL
# Info: gluino is a port of web2py libraries to 
# Bottle, Flask, Pyramid, Tornado, and other web frameworks.

import traceback
import threading

current = threading.local()
current.T = lambda message,*a,**b: str(message)

from dal import *
from template import *
from html import *
from http import redirect
from validators import *
from sqlhtml import *
from cache import Cache

cache = Cache(None)

class wrapper(object):
    debug = False
    response = None
    redirect = None
    http_handler = None 
    def __init__(self,view=None,dbs=[], debug = None, response = None):
        self.view = view
        self.dbs = dbs
        if not debug is None: self.debug = debug
        if not response is None: self.response = response
    def __call__(self,f):
        def g(*a,**b):
            g.__name__ = f.__name__
            try:
                r = f(*a,**b)
                if self.view:
                    r = render(filename=self.view,context=r)
                if self.response:
                    # used by pyramid
                    r = self.response(r)
            except HTTP, http:
                if 300<=http.status<400 and self.redirect:
                    return self.redirect(http.status,http.headers['Location'])
                elif self.http_handler:
                    return self.http_handler(http.status,http.headers)
                else:
                    raise NotImplementedError
            except Exception, e:
                print e
                for db in self.dbs: db.rollback()
                if self.debug:
                    return str(traceback.format_exc())
                raise e
            for db in self.dbs: db.commit()
            if a and a[0].__class__.__name__=='MainHandler':
                # for tornado
                a[0].write(r)
            else:
                # for bottle, flask, pyramid
                return r
        return g
    
    @staticmethod
    def extract_vars(form):
        d = {}
        for key, value in form.items():
            if isinstance(value,list) and len(value)==1:
                value = value[0]
            if not key in d:
                d[key] = value
            elif isinstance(d[key],list):
                d[key].append(value)
            else:
                d[key]=[d[key],value]
        return d

