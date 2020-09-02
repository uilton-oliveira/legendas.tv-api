#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
import base64
from . import webservice
import json


def format_date(dt):
    return dt.strftime('%d/%m/%y %H:%M:%S')


def index(request):
    return render(request, 'home/home.html')


def guess(request, filename=None):
    if filename:
        return HttpResponse(webservice.guess(filename), content_type="application/json; charset=utf-8")
    else:
        return HttpResponse('', content_type="application/json; charset=utf-8")


def auto_detect(request, filename=None):
    if filename:
        return HttpResponse(webservice.auto_detect(filename), content_type="application/json; charset=utf-8")
    else:
        return HttpResponse('', content_type="application/json; charset=utf-8")


@csrf_exempt
def choose_best(request):
    data = request.POST.get("data", "")
    filename = request.POST.get("filename", "")
    if data and filename:
        decoded = json.loads(data)
        return HttpResponse(webservice.choose_best(decoded, filename), content_type="application/json; charset=utf-8")
    else:
        return HttpResponse('', content_type="application/json; charset=utf-8")


def home(request, search=None, page=1):
    try:
        search = base64.b64decode(search)
    except:
        pass

    result = webservice.search(search, page)

    return HttpResponse(result, content_type="application/json; charset=utf-8")
