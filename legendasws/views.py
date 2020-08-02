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


def autodetect(request, filename=None):
    if filename:
        return HttpResponse(webservice.autodetect(filename), content_type="application/json; charset=utf-8")
    else:
        return HttpResponse('', content_type="application/json; charset=utf-8")


@csrf_exempt
def choosebest(request):
    data = request.POST.get("data", "")
    filename = request.POST.get("filename", "")
    if data and filename:
        decoded = json.loads(data)
        return HttpResponse(webservice.choosebest(decoded, filename), content_type="application/json; charset=utf-8")
    else:
        return HttpResponse('', content_type="application/json; charset=utf-8")


def home(request, busca=None, pagina=1):
    try:
        busca = base64.b64decode(busca)
    except:
        pass

    result = webservice.gerar(busca, pagina)

    return HttpResponse(result, content_type="application/json; charset=utf-8")
