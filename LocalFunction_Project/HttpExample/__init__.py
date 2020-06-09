import logging
import azure.functions as func
import mimetypes
import os
import json
from .test123 import *
import pathlib
import datetime


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
    a = CoronaUpdate(name)
    htmlpage = a.sub_data()
    html = func.HttpResponse(htmlpage, mimetype='text/html')
    return html
    #file = pathlib.Path(__file__).parent / 'State13.html'
    #file = 'HttpExample/index.html'

    '''
    with open(file, 'rb') as f:
        #mimetype = mimetypes.guess_type(file)
        #html = func.HttpResponse(f.read(), mimetype=mimetype[0])
        html = func.HttpResponse(f.read(), mimetype= 'text/html')
        return html
    '''
